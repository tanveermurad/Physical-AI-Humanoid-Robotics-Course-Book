# Authentication System Setup Guide

This guide will help you set up the authentication system with Better Auth for the Physical AI & Humanoid Robotics Course Book.

## Overview

The authentication system consists of:
- **Auth Server**: Node.js/Express server using Better Auth
- **Frontend**: Docusaurus site with React components
- **Features**: Sign up with background questionnaire, sign in, user profiles, personalized content

## Prerequisites

- Node.js 20+ installed
- npm or yarn package manager
- Two terminal windows (one for auth server, one for frontend)

## Step 1: Install Auth Server Dependencies

**Note**: There may be SSL/network issues when installing. If you encounter errors, try these commands:

```bash
cd auth-server

# Try standard install first
npm install

# If that fails, try with legacy peer deps
npm install --legacy-peer-deps

# If still failing, clear cache and retry
npm cache clean --force
npm install --legacy-peer-deps
```

The required dependencies are:
- `better-auth` - Authentication library
- `express` - Web server
- `cors` - Cross-origin resource sharing
- `dotenv` - Environment variables
- `better-sqlite3` - Database

## Step 2: Configure Environment Variables

1. Copy the example environment file:
```bash
cd auth-server
cp .env.example .env
```

2. Generate a secure secret key:
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

3. Edit `.env` and update the `BETTER_AUTH_SECRET` with the generated key:
```env
BETTER_AUTH_SECRET=your-generated-secret-key-here
BETTER_AUTH_URL=http://localhost:3001
DATABASE_URL=./auth.db
FRONTEND_URL=http://localhost:3000
PORT=3001
```

## Step 3: Start the Auth Server

```bash
cd auth-server
npm run dev
```

The auth server will start on `http://localhost:3001`.

You should see:
```
Auth server running on http://localhost:3001
Better Auth API available at http://localhost:3001/api/auth/*
```

## Step 4: Start the Frontend

In a **new terminal window**:

```bash
cd my-book
npm start
```

The Docusaurus site will start on `http://localhost:3000`.

## Testing the System

### 1. Sign Up Flow

1. Navigate to `http://localhost:3000/signup`
2. Fill in the 4-step questionnaire:
   - **Step 1**: Basic info (name, email, password)
   - **Step 2**: Software background (programming experience, languages, AI/ML, ROS)
   - **Step 3**: Hardware background (robotics experience, projects, hardware ownership)
   - **Step 4**: Learning preferences (goals, difficulty level)
3. Click "Create Account"
4. You'll be redirected to the home page, logged in

### 2. Sign In

1. Navigate to `http://localhost:3000/signin`
2. Enter your email and password
3. Click "Sign In"

### 3. View Profile

1. After signing in, click your name in the top navigation
2. Click "Profile"
3. View your background information
4. Click "Edit Profile" to modify your information

### 4. Chapter Personalization

To use the personalization feature in your documentation:

```mdx
---
title: Your Chapter Title
---

import PersonalizeChapter from '@site/src/components/PersonalizeChapter';

# Chapter Title

<PersonalizeChapter chapter="1" topic="ROS 2 Fundamentals" />

Your chapter content here...
```

When users click "Personalize This Chapter", they'll see:
- Personalized tips based on their experience level
- Recommended exercises tailored to their background
- Additional resources matched to their learning goals

## Authentication API Endpoints

The auth server provides these endpoints:

### Better Auth Endpoints (handled automatically)
- `POST /api/auth/sign-up` - Create new user account
- `POST /api/auth/sign-in` - Sign in with email/password
- `POST /api/auth/sign-out` - Sign out
- `GET /api/auth/session` - Get current session

### Custom Endpoints
- `GET /api/user/profile` - Get user profile with background data
- `PATCH /api/user/profile` - Update user profile and background

## User Profile Schema

Users have the following profile fields:

### Basic Info
- `id`: string
- `email`: string
- `name`: string
- `createdAt`: date
- `updatedAt`: date

### Software Background
- `programmingExperience`: 'beginner' | 'intermediate' | 'advanced' | 'expert'
- `programmingLanguages`: string[] (e.g., ['Python', 'C++'])
- `aiMlExperience`: 'none' | 'basic' | 'intermediate' | 'advanced'
- `rosExperience`: 'none' | 'basic' | 'intermediate' | 'advanced'

### Hardware Background
- `roboticsExperience`: 'none' | 'hobbyist' | 'student' | 'professional'
- `hardwareProjects`: string[] (e.g., ['Arduino/Raspberry Pi', 'Robot Kits'])
- `hasRoboticsHardware`: boolean
- `hardwareDescription`: string (optional description of their hardware)

### Learning Preferences
- `learningGoals`: string[] (e.g., ['Humanoid Robotics', 'ROS 2'])
- `preferredDifficulty`: 'beginner' | 'intermediate' | 'advanced'
- `onboardingCompleted`: boolean

## Personalization Logic

The `PersonalizeChapter` component generates personalized content based on:

1. **Programming Experience**: Adjusts complexity of tips and exercises
2. **ROS Experience**: Shows/hides ROS basics, provides relevant resources
3. **Hardware Availability**: Suggests hardware experiments or simulation alternatives
4. **AI/ML Experience**: Provides foundational resources if needed
5. **Learning Goals**: Highlights relevant sections aligned with their goals
6. **Difficulty Preference**: Recommends appropriate challenge level

## Production Deployment

### Security Considerations

1. **Use HTTPS**: Always use HTTPS in production
2. **Strong Secret**: Generate a cryptographically secure secret for `BETTER_AUTH_SECRET`
3. **CORS**: Update `FRONTEND_URL` to your production domain
4. **Email Verification**: Enable email verification in `auth-server/index.js`:
   ```javascript
   emailAndPassword: {
     enabled: true,
     requireEmailVerification: true, // Change to true
   }
   ```

### Database

For production, consider upgrading from SQLite to PostgreSQL:

1. Install PostgreSQL adapter:
```bash
npm install pg
```

2. Update `auth-server/index.js`:
```javascript
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

export const auth = betterAuth({
  database: pool,
  // ... rest of config
});
```

3. Update `DATABASE_URL` in `.env`:
```env
DATABASE_URL=postgresql://user:password@host:5432/database
```

## Troubleshooting

### Auth server won't start

**Error**: `Module not found: better-auth`
**Solution**: Ensure you've run `npm install` in the `auth-server` directory

**Error**: SSL cipher operation failed
**Solution**: Try clearing npm cache and reinstalling:
```bash
npm cache clean --force
npm install --legacy-peer-deps
```

### Frontend TypeScript errors

If you see TypeScript errors about missing types:
```bash
cd my-book
npm install --save-dev @types/react @types/react-dom
```

### CORS errors

**Error**: Cross-origin request blocked
**Solution**: Ensure `FRONTEND_URL` in auth-server `.env` matches your frontend URL

### Database errors

**Error**: `SQLITE_CANTOPEN`
**Solution**: Ensure the auth-server has write permissions in its directory

### Session not persisting

**Error**: User logs in but session doesn't persist
**Solution**:
1. Check that cookies are enabled in your browser
2. Ensure both auth server and frontend are on localhost (or both on the same domain)
3. Check browser console for cookie-related errors

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Docusaurus)                 │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │  SignUp Page   │  │ SignIn Page  │  │  Profile Page   │ │
│  └────────────────┘  └──────────────┘  └─────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            PersonalizeChapter Component                 │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              AuthContext (Global State)                 │ │
│  └────────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP Requests
                            │ (with credentials)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               Auth Server (Node.js + Better Auth)            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               Better Auth Core                        │  │
│  │  • Session Management                                 │  │
│  │  • Password Hashing                                   │  │
│  │  • Cookie Management                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Custom Profile API                         │  │
│  │  • GET  /api/user/profile                            │  │
│  │  • PATCH /api/user/profile                           │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │ SQLite / PostgreSQL
                            ▼
                    ┌─────────────────┐
                    │    Database     │
                    │  • users        │
                    │  • sessions     │
                    └─────────────────┘
```

## Next Steps

1. **Add Email Verification**: Set up SMTP for email verification
2. **OAuth Providers**: Add Google/GitHub sign-in via Better Auth plugins
3. **Password Reset**: Implement forgot password flow
4. **Profile Pictures**: Add avatar upload functionality
5. **Admin Dashboard**: Create admin panel for user management

## Support

For issues or questions:
- Better Auth Docs: https://www.better-auth.com/docs
- Docusaurus Docs: https://docusaurus.io/docs
- GitHub Issues: Create an issue in your repository
