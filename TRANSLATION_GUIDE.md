# Urdu Translation Feature Guide

This guide explains how to add Urdu translation capabilities to your course chapters, allowing logged-in users to translate content with a single click.

## Overview

The translation system allows users to:
- ✅ Translate entire chapters to Urdu
- ✅ Toggle between English and Urdu
- ✅ Preserve code blocks and technical terms
- ✅ Use context-aware translation (requires integration with translation API)

## Prerequisites

- User must be logged in to use translation feature
- Auth server must be running on `http://localhost:3001`
- Translation endpoint configured in auth server

## Basic Usage

### Adding Translation to a Chapter

Add these components at the start of your MDX file:

```mdx
---
title: Your Chapter Title
---

import PersonalizeChapter from '@site/src/components/PersonalizeChapter';
import TranslateChapter from '@site/src/components/TranslateChapter';

# Your Chapter Title

<TranslateChapter chapter="1" title="Introduction to ROS 2" />
<PersonalizeChapter chapter="1" topic="ROS 2 Fundamentals" />

Your chapter content goes here...
```

### Props

The `TranslateChapter` component accepts:

- **`chapter`** (string, required): Chapter number/identifier (e.g., "1", "2.3")
- **`title`** (string, required): Full chapter title for context
- **`contentSelector`** (string, optional): CSS selector for content to translate (default: `.markdown`)

## Complete Example

```mdx
---
title: ROS 2 Architecture and Core Concepts
sidebar_position: 3
---

import PersonalizeChapter from '@site/src/components/PersonalizeChapter';
import TranslateChapter from '@site/src/components/TranslateChapter';

# Chapter 3: ROS 2 Architecture and Core Concepts

<TranslateChapter
  chapter="3"
  title="ROS 2 Architecture and Core Concepts"
/>

<PersonalizeChapter
  chapter="3"
  topic="ROS 2 Architecture"
/>

## Introduction

ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software...

## Nodes

In ROS 2, a **node** is a fundamental building block...

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        self.get_logger().info('Node started')
```

The code above demonstrates...
```

## What Happens When Users Click Translate

### Step 1: Before Translation
```
┌─────────────────────────────────────────┐
│  🌐 اردو میں پڑھیں | Translate to Urdu  │
│                                          │
│  Sign in to translate this chapter      │
│  to Urdu                                 │
└─────────────────────────────────────────┘
```

### Step 2: During Translation
```
┌─────────────────────────────────────────┐
│  ⏳ ترجمہ ہو رہا ہے... Translating...    │
└─────────────────────────────────────────┘
```

### Step 3: After Translation
```
┌─────────────────────────────────────────┐
│  🔄 Show English | انگریزی میں دیکھیں   │
│                                          │
│  ✓ Content translated to Urdu |         │
│    مواد اردو میں ترجمہ کیا گیا          │
└─────────────────────────────────────────┘
```

The page content will be displayed in Urdu with right-to-left text direction.

### Step 4: Toggle Back to English
Users can click the button again to restore the original English content.

## How Translation Works

### 1. Content Extraction
```javascript
// Component extracts text nodes from the page
const elementsToTranslate = [];
extractTextNodes(contentElement);
```

### 2. Smart Filtering
- ✅ **Translates**: Headings, paragraphs, lists, captions
- ❌ **Preserves**: Code blocks, commands, URLs, technical identifiers

### 3. Batch Translation
```javascript
// Groups texts into batches of 10 for efficiency
const batches = groupIntoBatches(texts, 10);

for (const batch of batches) {
  const translations = await translateBatch(batch);
  applyTranslations(translations);
}
```

### 4. DOM Update
- Original content is saved
- Translated text replaces English text
- Page direction changes to RTL (right-to-left)
- Urdu font family is applied

## Translation API

### Endpoint
```
POST http://localhost:3001/api/translate
```

### Request Format
```json
{
  "texts": [
    "Introduction to ROS 2",
    "ROS 2 is a flexible framework",
    "Let's explore the core concepts"
  ],
  "targetLanguage": "urdu",
  "chapter": "3",
  "title": "ROS 2 Architecture"
}
```

### Response Format
```json
{
  "translations": [
    "ROS 2 کا تعارف",
    "ROS 2 ایک لچکدار فریم ورک ہے",
    "آئیے بنیادی تصورات کو دریافت کریں"
  ],
  "sourceLanguage": "en",
  "targetLanguage": "ur",
  "chapter": "3",
  "title": "ROS 2 Architecture"
}
```

## Integrating Real Translation Services

The current implementation uses a placeholder. To integrate real translation:

### Option 1: Google Cloud Translation API

1. Install the package:
```bash
cd auth-server
npm install @google-cloud/translate
```

2. Update `auth-server/index.js`:
```javascript
import { Translate } from '@google-cloud/translate/v2';

const translate = new Translate({
  projectId: process.env.GOOGLE_CLOUD_PROJECT_ID,
  keyFilename: process.env.GOOGLE_CLOUD_KEY_FILE,
});

app.post('/api/translate', async (req, res) => {
  const { texts, targetLanguage } = req.body;

  try {
    const [translations] = await translate.translate(texts, 'ur');
    res.json({ translations });
  } catch (error) {
    console.error('Translation error:', error);
    res.status(500).json({ error: 'Translation failed' });
  }
});
```

3. Set environment variables in `.env`:
```env
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_KEY_FILE=path/to/service-account-key.json
```

### Option 2: OpenAI GPT (Context-Aware)

1. Install OpenAI package:
```bash
cd auth-server
npm install openai
```

2. Update `auth-server/index.js`:
```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

app.post('/api/translate', async (req, res) => {
  const { texts, chapter, title } = req.body;

  try {
    const prompt = `Translate the following robotics/AI course content from English to Urdu.
Context: Chapter ${chapter} - "${title}"
Preserve technical terms like "ROS 2", "node", "topic", etc.

Texts to translate:
${texts.map((t, i) => `${i + 1}. ${t}`).join('\n')}

Provide translations in the same order, one per line:`;

    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: 'You are a technical translator specializing in robotics and AI content. Translate to formal Urdu while preserving English technical terms.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
    });

    const translations = completion.choices[0].message.content
      .split('\n')
      .map(line => line.replace(/^\d+\.\s*/, '').trim());

    res.json({ translations });
  } catch (error) {
    console.error('Translation error:', error);
    res.status(500).json({ error: 'Translation failed' });
  }
});
```

3. Set API key in `.env`:
```env
OPENAI_API_KEY=your-openai-api-key
```

### Option 3: Microsoft Translator API

1. Install the package:
```bash
cd auth-server
npm install @azure/ai-translation-text
```

2. Update `auth-server/index.js`:
```javascript
import { TextTranslationClient, isUnexpected } from '@azure/ai-translation-text';

const client = new TextTranslationClient(
  process.env.AZURE_TRANSLATOR_KEY,
  process.env.AZURE_TRANSLATOR_REGION
);

app.post('/api/translate', async (req, res) => {
  const { texts } = req.body;

  try {
    const response = await client.path('/translate').post({
      body: texts.map(text => ({ text })),
      queryParameters: {
        to: 'ur',
        from: 'en',
      },
    });

    if (isUnexpected(response)) {
      throw new Error('Translation failed');
    }

    const translations = response.body.map(item => item.translations[0].text);
    res.json({ translations });
  } catch (error) {
    console.error('Translation error:', error);
    res.status(500).json({ error: 'Translation failed' });
  }
});
```

3. Set credentials in `.env`:
```env
AZURE_TRANSLATOR_KEY=your-translator-key
AZURE_TRANSLATOR_REGION=your-region
```

## Pre-translated Content (Alternative Approach)

For better performance and quality, consider pre-translating content:

### 1. Create Urdu Versions

```
docs/
  ├── intro.md (English)
  ├── intro.ur.md (Urdu)
  ├── ros2-basics.md (English)
  └── ros2-basics.ur.md (Urdu)
```

### 2. Modify Component to Load Pre-translated Files

```typescript
const loadPreTranslated = async (chapter: string) => {
  const response = await fetch(`/docs/${chapter}.ur.md`);
  if (response.ok) {
    const urduContent = await response.text();
    return urduContent;
  }
  return null;
};
```

Benefits:
- ✅ Faster (no API calls)
- ✅ Better quality (human-reviewed translations)
- ✅ No API costs
- ✅ Works offline

Drawbacks:
- ❌ Requires manual translation work
- ❌ Harder to maintain (two versions of every chapter)

## Styling and Typography

### Urdu Font

The component automatically applies Urdu-friendly fonts:

```css
font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', Arial, sans-serif;
```

To use custom Urdu fonts, add them to `docusaurus.config.ts`:

```typescript
stylesheets: [
  {
    href: 'https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu&display=swap',
    type: 'text/css',
  },
],
```

### RTL (Right-to-Left) Layout

When translated, content automatically switches to RTL:

```css
.translated {
  direction: rtl;
  text-align: right;
}
```

### Preserving Code Blocks

Code blocks remain LTR (left-to-right) even in translated content:

```css
.translated code,
.translated pre {
  direction: ltr;
  text-align: left;
}
```

## Best Practices

### 1. Test with Real Users
- Have native Urdu speakers review translations
- Check readability on mobile devices
- Ensure technical terms make sense

### 2. Handle Mixed Content
- Keep English terms that don't translate well (e.g., "ROS 2", "Gazebo")
- Use parentheses for clarification: "نوڈ (node)"

### 3. Performance Optimization
- Cache translations in localStorage
- Use batch translation (10-20 texts per request)
- Show progress indicator for long chapters

### 4. Accessibility
- Maintain proper heading hierarchy in translations
- Ensure links work in both languages
- Test with screen readers

## Troubleshooting

### Translation Button Not Appearing
**Issue**: Button doesn't show up
**Solution**: Ensure you're importing the component correctly and user is logged in

### Translation Fails
**Issue**: Error during translation
**Solution**: Check auth server is running, user session is valid, and translation API is configured

### Mixed Direction Issues
**Issue**: Some text appears LTR in RTL mode
**Solution**: Ensure proper CSS for code blocks and technical terms

### Font Not Loading
**Issue**: Urdu text appears in wrong font
**Solution**: Add Urdu font to `docusaurus.config.ts` stylesheets

## Example: Full Chapter with Both Features

```mdx
---
title: Computer Vision for Humanoid Robots
sidebar_position: 8
---

import PersonalizeChapter from '@site/src/components/PersonalizeChapter';
import TranslateChapter from '@site/src/components/TranslateChapter';

# Chapter 8: Computer Vision for Humanoid Robots

<TranslateChapter
  chapter="8"
  title="Computer Vision for Humanoid Robots"
/>

<PersonalizeChapter
  chapter="8"
  topic="Computer Vision and Perception"
/>

## Introduction

Computer vision enables robots to perceive and understand their environment...

## Object Detection

Object detection is the process of identifying and locating objects...

```python
import cv2
import numpy as np

# Load pre-trained model
model = cv2.dnn.readNet('model.weights', 'model.cfg')

# Process image
blob = cv2.dnn.blobFromImage(image)
model.setInput(blob)
outputs = model.forward()
```

The code demonstrates how to use OpenCV for object detection...

## Exercises

1. Implement a face detection system
2. Create an object tracking pipeline
3. Build a gesture recognition module
```

## Future Enhancements

Potential improvements:
1. **Voice Output**: Text-to-speech for Urdu content
2. **Multiple Languages**: Support Arabic, Hindi, Bengali
3. **Collaborative Translation**: Community can suggest improvements
4. **Translation Memory**: Reuse previous translations for consistency
5. **Offline Mode**: Download translated chapters for offline reading

## Costs and Considerations

### Google Cloud Translation
- **Cost**: $20 per million characters
- **Quality**: Good for general content
- **Speed**: Fast

### OpenAI GPT-4
- **Cost**: ~$0.03 per 1K tokens (input) + $0.06 per 1K tokens (output)
- **Quality**: Excellent, context-aware
- **Speed**: Moderate

### Microsoft Translator
- **Cost**: $10 per million characters
- **Quality**: Good
- **Speed**: Fast

### Pre-translated Content
- **Cost**: Translation service cost (one-time) + maintenance
- **Quality**: Best (human-reviewed)
- **Speed**: Instant (no API calls)

## Conclusion

The Urdu translation feature makes your robotics course accessible to Urdu-speaking students worldwide. Start with placeholder translation during development, then integrate a real translation API for production.
