# How to Add Personalization to Your Chapters

This guide shows you how to add the personalization feature to any chapter in your documentation.

## Basic Usage

Add this import at the top of your MDX file:

```mdx
---
title: Your Chapter Title
---

import PersonalizeChapter from '@site/src/components/PersonalizeChapter';

# Your Chapter Title

<PersonalizeChapter chapter="1" topic="Introduction to ROS 2" />

Your regular chapter content goes here...
```

## Props

The `PersonalizeChapter` component accepts two props:

- `chapter` (string): The chapter number or identifier (e.g., "1", "2", "3.1")
- `topic` (string): The chapter topic name (e.g., "ROS 2 Fundamentals", "Computer Vision", "SLAM")

The `topic` prop is used to provide context-specific personalization based on keywords.

## Example 1: ROS 2 Chapter

```mdx
---
title: ROS 2 Fundamentals
---

import PersonalizeChapter from '@site/src/components/PersonalizeChapter';

# Chapter 3: ROS 2 Fundamentals

<PersonalizeChapter chapter="3" topic="ROS 2 Fundamentals" />

## Introduction

ROS 2 (Robot Operating System 2) is a flexible framework...
```

**Personalization behavior**:
- Users with **no ROS experience** see: Tips about ROS learning curve, links to tutorials
- Users with **advanced ROS experience** see: Suggestions to skip basics, focus on advanced patterns
- Users who selected **"ROS 2" as a learning goal** see: Special emphasis that this aligns with their goals

## Example 2: Computer Vision Chapter

```mdx
---
title: Computer Vision for Robotics
---

import PersonalizeChapter from '@site/src/components/PersonalizeChapter';

# Chapter 8: Computer Vision for Robotics

<PersonalizeChapter chapter="8" topic="Computer Vision and Perception" />

## Overview

Computer vision is essential for robots to perceive...
```

**Personalization behavior**:
- Users who selected **"Computer Vision"** as a goal see: Highlighted importance
- Users with **no AI/ML experience** see: Links to ML crash course
- Users with **camera hardware** see: Suggestions to test on their setup

## Example 3: Simulation Chapter

```mdx
---
title: Gazebo and Isaac Sim
---

import PersonalizeChapter from '@site/src/components/PersonalizeChapter';

# Chapter 5: Robot Simulation

<PersonalizeChapter chapter="5" topic="Simulation with Gazebo and Isaac Sim" />

## Why Simulation Matters

Simulation allows us to test robots safely...
```

**Personalization behavior**:
- Users **with hardware** see: Encouragement to test concepts on real hardware after simulation
- Users **without hardware** see: Focus on simulation as the primary learning tool
- Users who selected **"Simulation"** as a goal see: Extra encouragement to explore advanced features

## Personalization Logic

The component personalizes content based on:

### 1. Programming Experience
- **Beginners**: Step-by-step guidance, focus on fundamentals
- **Advanced/Expert**: Optimization tips, advanced challenges

### 2. ROS Experience
- **None**: ROS tutorials, learning curve warnings
- **Advanced**: Skip basics, advanced implementation patterns

### 3. AI/ML Experience
- **None**: Machine learning basics resources
- **Advanced**: Advanced techniques and optimizations

### 4. Hardware Availability
- **Has hardware**: Try on real hardware, hardware-specific tips
- **No hardware**: Focus on simulation, simulation tutorials

### 5. Learning Goals
- Highlights chapters that match their selected goals
- Provides relevant exercises and extensions

### 6. Difficulty Preference
- **Beginner**: Focus on "why" before "how"
- **Intermediate**: Balanced approach
- **Advanced**: Challenge with optional advanced sections

## What Users See

### When Not Signed In
```
┌─────────────────────────────────────────┐
│  ✨ Personalize This Chapter             │
│                                          │
│  Sign up to get personalized content    │
│  recommendations                         │
└─────────────────────────────────────────┘
```

### When Signed In (Before Clicking)
```
┌─────────────────────────────────────────┐
│  ✨ Personalize This Chapter             │
│                                          │
│  Get personalized tips, exercises, and  │
│  resources based on your background     │
└─────────────────────────────────────────┘
```

### After Personalizing
```
┌─────────────────────────────────────────┐
│  🎯 Personalized for You               ✕ │
├─────────────────────────────────────────┤
│  💡 Tips for Your Learning Path         │
│  • Focus on simulation - you can       │
│    implement everything in Gazebo      │
│  • ROS has a learning curve - focus on │
│    core concepts first                 │
│                                         │
│  🛠️ Recommended Exercises               │
│  • Complete the exercises at the end   │
│  • Start with simple modifications     │
│                                         │
│  📚 Additional Resources                │
│  • ROS Tutorials: wiki.ros.org         │
│  • Gazebo Tutorials: gazebosim.org     │
├─────────────────────────────────────────┤
│  Based on your profile: beginner        │
│  programmer, none ROS experience        │
└─────────────────────────────────────────┘
```

## Best Practices

### 1. Place at the Start
Put the component right after the chapter title, before the main content:

```mdx
# Chapter Title

<PersonalizeChapter chapter="X" topic="..." />

## First Section
```

### 2. Use Descriptive Topics
Use descriptive topic names that include relevant keywords:

✅ Good:
- `"ROS 2 and Robot Control"`
- `"Computer Vision and AI"`
- `"Gazebo Simulation"`

❌ Less effective:
- `"Chapter 3"`
- `"Part Two"`

### 3. One Per Chapter
Only use one `PersonalizeChapter` component per page/chapter.

## Styling Customization

The component uses CSS modules. To customize styling, edit:
```
my-book/src/components/PersonalizeChapter/styles.module.css
```

Key classes:
- `.personalizeButton` - The initial button container
- `.button` - The personalize button
- `.personalizedContent` - The expanded personalization box
- `.section` - Each section (tips, exercises, resources)

## Future Enhancements

Potential additions:
1. **AI-Generated Content**: Use OpenAI API to generate fully custom tips
2. **Progress Tracking**: Show which chapters they've completed
3. **Adaptive Difficulty**: Suggest easier/harder content based on progress
4. **Social Features**: See what other learners with similar backgrounds found helpful
5. **Spaced Repetition**: Remind users to review concepts based on their background

## Testing Tips

Test with different user profiles:
1. Create account with **beginner** programming, **no ROS** → See basic guidance
2. Create account with **expert** programming, **advanced ROS** → See advanced tips
3. Create account **with hardware** → See hardware-specific suggestions
4. Create account **without hardware** → See simulation focus
5. Select different **learning goals** → See goal-specific highlights
