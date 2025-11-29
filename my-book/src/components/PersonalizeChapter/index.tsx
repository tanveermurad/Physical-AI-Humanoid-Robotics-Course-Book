import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import styles from './styles.module.css';

interface PersonalizedContent {
  tips: string[];
  exercises: string[];
  resources: string[];
}

interface PersonalizeChapterProps {
  chapter: string;
  topic: string;
}

export default function PersonalizeChapter({ chapter, topic }: PersonalizeChapterProps) {
  const { user } = useAuth();
  const [personalized, setPersonalized] = useState<PersonalizedContent | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const generatePersonalizedContent = (): PersonalizedContent => {
    if (!user) return { tips: [], exercises: [], resources: [] };

    const content: PersonalizedContent = {
      tips: [],
      exercises: [],
      resources: [],
    };

    // Personalize based on programming experience
    if (user.programmingExperience === 'beginner') {
      content.tips.push('💡 Take time to understand each code example - don\'t rush through them');
      content.tips.push('📝 Try typing out the code yourself instead of copy-pasting to build muscle memory');
      content.exercises.push('Start with simple modifications to existing code examples');
    } else if (user.programmingExperience === 'advanced' || user.programmingExperience === 'expert') {
      content.tips.push('🚀 Focus on optimization and best practices in the advanced sections');
      content.exercises.push('Implement additional features beyond the basic requirements');
    }

    // Personalize based on ROS experience
    if (user.rosExperience === 'none' && topic.toLowerCase().includes('ros')) {
      content.tips.push('🤖 ROS has a learning curve - focus on understanding the core concepts first');
      content.resources.push('ROS Tutorials: http://wiki.ros.org/ROS/Tutorials');
    } else if (user.rosExperience === 'advanced' && topic.toLowerCase().includes('ros')) {
      content.tips.push('⚡ You can skip the basics - jump to the advanced implementation patterns');
    }

    // Personalize based on hardware availability
    if (user.hasRoboticsHardware) {
      content.exercises.push(`🔧 Try implementing this on your ${user.hardwareDescription || 'hardware'}`);
      content.tips.push('💻 Test this concept on your actual hardware for hands-on learning');
    } else {
      content.tips.push('🖥️ Focus on simulation - you can implement everything in Gazebo or Isaac Sim');
      content.resources.push('Gazebo Tutorials: https://gazebosim.org/docs');
    }

    // Personalize based on AI/ML experience
    if (user.aiMlExperience === 'none' && (topic.toLowerCase().includes('ai') || topic.toLowerCase().includes('ml'))) {
      content.tips.push('🧠 AI/ML concepts can be complex - take it step by step');
      content.resources.push('Machine Learning Basics: https://developers.google.com/machine-learning/crash-course');
    }

    // Personalize based on learning goals
    if (user.learningGoals?.includes('Computer Vision') && topic.toLowerCase().includes('vision')) {
      content.tips.push('👁️ This aligns with your computer vision learning goals - pay special attention!');
      content.exercises.push('Implement a computer vision-based feature as an extension');
    }

    if (user.learningGoals?.includes('Simulation (Gazebo/Isaac)') && (topic.toLowerCase().includes('gazebo') || topic.toLowerCase().includes('isaac'))) {
      content.tips.push('🎮 This aligns with your simulation learning goals - explore the advanced features!');
    }

    // Personalize based on difficulty preference
    if (user.preferredDifficulty === 'beginner') {
      content.tips.push('📚 Focus on understanding "why" before diving into "how"');
    } else if (user.preferredDifficulty === 'advanced') {
      content.tips.push('🎯 Challenge yourself with the optional advanced sections');
    }

    // Default helpful tips
    if (content.tips.length === 0) {
      content.tips.push('📖 Read through the entire chapter before starting the exercises');
    }

    if (content.exercises.length === 0) {
      content.exercises.push('Complete the exercises at the end of this chapter');
    }

    return content;
  };

  const handlePersonalize = () => {
    if (!user) {
      window.location.href = '/signup';
      return;
    }

    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      const content = generatePersonalizedContent();
      setPersonalized(content);
      setLoading(false);
    }, 500);
  };

  if (!personalized) {
    return (
      <div className={styles.personalizeButton}>
        <button onClick={handlePersonalize} disabled={loading} className={styles.button}>
          {loading ? '⏳ Personalizing...' : '✨ Personalize This Chapter'}
        </button>
        <p className={styles.hint}>
          {user
            ? 'Get personalized tips, exercises, and resources based on your background'
            : 'Sign up to get personalized content recommendations'}
        </p>
      </div>
    );
  }

  return (
    <div className={styles.personalizedContent}>
      <div className={styles.header}>
        <h3>🎯 Personalized for You</h3>
        <button onClick={() => setPersonalized(null)} className={styles.closeButton}>
          ✕
        </button>
      </div>

      {personalized.tips.length > 0 && (
        <div className={styles.section}>
          <h4>💡 Tips for Your Learning Path</h4>
          <ul>
            {personalized.tips.map((tip, index) => (
              <li key={index}>{tip}</li>
            ))}
          </ul>
        </div>
      )}

      {personalized.exercises.length > 0 && (
        <div className={styles.section}>
          <h4>🛠️ Recommended Exercises</h4>
          <ul>
            {personalized.exercises.map((exercise, index) => (
              <li key={index}>{exercise}</li>
            ))}
          </ul>
        </div>
      )}

      {personalized.resources.length > 0 && (
        <div className={styles.section}>
          <h4>📚 Additional Resources</h4>
          <ul>
            {personalized.resources.map((resource, index) => (
              <li key={index}>{resource}</li>
            ))}
          </ul>
        </div>
      )}

      <p className={styles.footer}>
        Based on your profile: {user?.programmingExperience} programmer, {user?.rosExperience} ROS experience
      </p>
    </div>
  );
}
