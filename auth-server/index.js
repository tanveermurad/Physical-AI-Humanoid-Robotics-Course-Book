import express from 'express';
import cors from 'cors';
import { betterAuth } from 'better-auth';
import Database from 'better-sqlite3';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Initialize Better Auth
export const auth = betterAuth({
  database: new Database(process.env.DATABASE_URL || './auth.db'),
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set to true in production
  },
  user: {
    additionalFields: {
      // These fields can be set during signup
      programmingExperience: {
        type: 'string',
        required: false,
      },
      programmingLanguages: {
        type: 'string',
        required: false,
      },
      aiMlExperience: {
        type: 'string',
        required: false,
      },
      rosExperience: {
        type: 'string',
        required: false,
      },
      roboticsExperience: {
        type: 'string',
        required: false,
      },
      hardwareProjects: {
        type: 'string',
        required: false,
      },
      hasRoboticsHardware: {
        type: 'boolean',
        required: false,
      },
      hardwareDescription: {
        type: 'string',
        required: false,
      },
      learningGoals: {
        type: 'string',
        required: false,
      },
      preferredDifficulty: {
        type: 'string',
        required: false,
      },
      onboardingCompleted: {
        type: 'boolean',
        defaultValue: false,
      },
    },
  },
  trustedOrigins: [
    process.env.FRONTEND_URL || 'http://localhost:3000',
  ],
});

// Middleware
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true,
}));
app.use(express.json());

// Mount Better Auth routes
app.all('/api/auth/*', async (req, res) => {
  return auth.handler(req, res);
});

// Custom endpoint to get user profile
app.get('/api/user/profile', async (req, res) => {
  try {
    const session = await auth.api.getSession({
      headers: req.headers,
    });

    if (!session) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    // Return user with profile data
    res.json({
      user: session.user,
    });
  } catch (error) {
    console.error('Error fetching profile:', error);
    res.status(500).json({ error: 'Failed to fetch profile' });
  }
});

// Custom endpoint to update user profile
app.patch('/api/user/profile', async (req, res) => {
  try {
    const session = await auth.api.getSession({
      headers: req.headers,
    });

    if (!session) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const {
      programmingExperience,
      programmingLanguages,
      aiMlExperience,
      rosExperience,
      roboticsExperience,
      hardwareProjects,
      hasRoboticsHardware,
      hardwareDescription,
      learningGoals,
      preferredDifficulty,
      onboardingCompleted,
    } = req.body;

    // Update user fields
    const updatedUser = await auth.api.updateUser({
      userId: session.user.id,
      data: {
        programmingExperience,
        programmingLanguages: JSON.stringify(programmingLanguages),
        aiMlExperience,
        rosExperience,
        roboticsExperience,
        hardwareProjects: JSON.stringify(hardwareProjects),
        hasRoboticsHardware,
        hardwareDescription,
        learningGoals: JSON.stringify(learningGoals),
        preferredDifficulty,
        onboardingCompleted,
      },
    });

    res.json({ user: updatedUser });
  } catch (error) {
    console.error('Error updating profile:', error);
    res.status(500).json({ error: 'Failed to update profile' });
  }
});

// Translation endpoint
app.post('/api/translate', async (req, res) => {
  try {
    const session = await auth.api.getSession({
      headers: req.headers,
    });

    if (!session) {
      return res.status(401).json({ error: 'Unauthorized. Please sign in to use translation.' });
    }

    const { texts, targetLanguage, chapter, title } = req.body;

    if (!texts || !Array.isArray(texts)) {
      return res.status(400).json({ error: 'Invalid request. texts must be an array.' });
    }

    // For now, return a placeholder response
    // In production, you would integrate with a translation API like:
    // - Google Cloud Translation API
    // - OpenAI GPT for context-aware translation
    // - Microsoft Translator API

    // Placeholder: For demonstration, we'll just add "Urdu: " prefix
    // In production, replace this with actual translation service
    const translations = texts.map(text => {
      // This is a placeholder - implement actual translation here
      return `[اردو] ${text}`;
    });

    res.json({
      translations,
      sourceLanguage: 'en',
      targetLanguage: targetLanguage || 'ur',
      chapter,
      title,
    });
  } catch (error) {
    console.error('Translation error:', error);
    res.status(500).json({ error: 'Translation service error' });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(PORT, () => {
  console.log(`Auth server running on http://localhost:${PORT}`);
  console.log(`Better Auth API available at http://localhost:${PORT}/api/auth/*`);
  console.log(`Translation API available at http://localhost:${PORT}/api/translate`);
});
