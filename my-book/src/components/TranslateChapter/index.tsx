import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import styles from './styles.module.css';

interface TranslateChapterProps {
  chapter: string;
  title: string;
  contentSelector?: string; // CSS selector for the content to translate
}

export default function TranslateChapter({
  chapter,
  title,
  contentSelector = '.markdown'
}: TranslateChapterProps) {
  const { user } = useAuth();
  const [translating, setTranslating] = useState(false);
  const [translated, setTranslated] = useState(false);
  const [error, setError] = useState('');
  const [originalContent, setOriginalContent] = useState<string>('');

  const translateToUrdu = async () => {
    if (!user) {
      window.location.href = '/signup';
      return;
    }

    setTranslating(true);
    setError('');

    try {
      // Get the content to translate
      const contentElement = document.querySelector(contentSelector);
      if (!contentElement) {
        throw new Error('Content not found');
      }

      // Save original content if not already saved
      if (!originalContent) {
        setOriginalContent(contentElement.innerHTML);
      }

      // Get all text nodes and their parent elements
      const elementsToTranslate: Array<{element: HTMLElement, text: string, isCode: boolean}> = [];

      const extractTextNodes = (node: Node, isCodeBlock: boolean = false) => {
        // Skip code blocks, pre tags, and script tags
        if (node.nodeName === 'CODE' || node.nodeName === 'PRE' || node.nodeName === 'SCRIPT') {
          return;
        }

        // Check if we're in a code block
        const inCodeBlock = isCodeBlock ||
          (node.parentElement?.classList.contains('prism-code') ||
           node.parentElement?.tagName === 'CODE' ||
           node.parentElement?.tagName === 'PRE');

        if (node.nodeType === Node.TEXT_NODE) {
          const text = node.textContent?.trim();
          if (text && text.length > 0 && !inCodeBlock) {
            elementsToTranslate.push({
              element: node.parentElement as HTMLElement,
              text: text,
              isCode: false
            });
          }
        } else if (node.nodeType === Node.ELEMENT_NODE) {
          const element = node as HTMLElement;
          // Don't translate code blocks
          if (element.tagName !== 'CODE' && element.tagName !== 'PRE') {
            node.childNodes.forEach(child => extractTextNodes(child, inCodeBlock));
          }
        }
      };

      extractTextNodes(contentElement);

      // Group translations into batches for efficiency
      const batchSize = 10;
      const batches: string[][] = [];

      for (let i = 0; i < elementsToTranslate.length; i += batchSize) {
        batches.push(elementsToTranslate.slice(i, i + batchSize).map(e => e.text));
      }

      // Translate each batch
      let translationIndex = 0;

      for (const batch of batches) {
        const response = await fetch('http://localhost:3001/api/translate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
          body: JSON.stringify({
            texts: batch,
            targetLanguage: 'urdu',
            chapter,
            title
          }),
        });

        if (!response.ok) {
          throw new Error('Translation service unavailable. Using fallback translation.');
        }

        const data = await response.json();
        const translations = data.translations;

        // Apply translations to the DOM
        for (let i = 0; i < translations.length; i++) {
          const item = elementsToTranslate[translationIndex + i];
          if (item && item.element) {
            // Find and replace the text node
            const walker = document.createTreeWalker(
              item.element,
              NodeFilter.SHOW_TEXT,
              null
            );

            let textNode;
            while (textNode = walker.nextNode()) {
              if (textNode.textContent?.trim() === item.text) {
                textNode.textContent = translations[i];
                break;
              }
            }
          }
        }

        translationIndex += batch.length;
      }

      setTranslated(true);
    } catch (err) {
      console.error('Translation error:', err);
      setError('Translation service is currently unavailable. Please try again later.');

      // Fallback: Show a simple placeholder translation
      // In production, you'd have pre-translated content or a different translation service
      setError('براہ کرم نوٹ کریں: فی الوقت ترجمہ کی سروس دستیاب نہیں ہے۔');
    } finally {
      setTranslating(false);
    }
  };

  const restoreOriginal = () => {
    if (originalContent) {
      const contentElement = document.querySelector(contentSelector);
      if (contentElement) {
        contentElement.innerHTML = originalContent;
        setTranslated(false);
      }
    }
  };

  const toggleLanguage = () => {
    if (translated) {
      restoreOriginal();
    } else {
      translateToUrdu();
    }
  };

  if (!user) {
    return (
      <div className={styles.translateButton}>
        <button onClick={() => window.location.href = '/signup'} className={styles.button}>
          🌐 اردو میں پڑھیں | Translate to Urdu
        </button>
        <p className={styles.hint}>
          Sign in to translate this chapter to Urdu
        </p>
      </div>
    );
  }

  return (
    <div className={styles.translateButton}>
      <button
        onClick={toggleLanguage}
        disabled={translating}
        className={translated ? styles.buttonActive : styles.button}
      >
        {translating ? '⏳ ترجمہ ہو رہا ہے... Translating...' :
         translated ? '🔄 Show English | انگریزی میں دیکھیں' :
         '🌐 اردو میں پڑھیں | Translate to Urdu'}
      </button>
      {error && <p className={styles.error}>{error}</p>}
      {translated && (
        <p className={styles.hint}>
          ✓ Content translated to Urdu | مواد اردو میں ترجمہ کیا گیا
        </p>
      )}
    </div>
  );
}
