# Authentication Server

This is a Node.js authentication server using [Better Auth](https://www.better-auth.com/).

## Setup

1. Install dependencies:
```bash
npm install
```

2. Copy `.env.example` to `.env` and update values:
```bash
cp .env.example .env
```

3. Generate a secure secret key for `BETTER_AUTH_SECRET` in `.env`:
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

4. Start the server:
```bash
npm run dev
```

The server will run on `http://localhost:3001`.

## Endpoints

- `POST /api/auth/sign-up` - Register a new user with background information
- `POST /api/auth/sign-in` - Sign in with email and password
- `POST /api/auth/sign-out` - Sign out
- `GET /api/user/profile` - Get current user profile
- `PATCH /api/user/profile` - Update user profile and background

## User Background Fields

During signup or profile update, you can provide:

### Software Background
- `programmingExperience`: beginner | intermediate | advanced | expert
- `programmingLanguages`: array of languages (stored as JSON string)
- `aiMlExperience`: none | basic | intermediate | advanced
- `rosExperience`: none | basic | intermediate | advanced

### Hardware Background
- `roboticsExperience`: none | hobbyist | student | professional
- `hardwareProjects`: array of projects (stored as JSON string)
- `hasRoboticsHardware`: boolean
- `hardwareDescription`: string

### Learning Preferences
- `learningGoals`: array of goals (stored as JSON string)
- `preferredDifficulty`: beginner | intermediate | advanced
- `onboardingCompleted`: boolean
