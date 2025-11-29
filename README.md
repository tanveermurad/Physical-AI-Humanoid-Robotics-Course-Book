# Physical AI & Humanoid Robotics Course Book

A comprehensive, interactive course book on Physical AI and Humanoid Robotics built with Docusaurus, featuring user authentication, personalized learning paths, Urdu translation, and an AI-powered chatbot.

## 🌟 Features

### 1. **User Authentication & Profiles**
- Sign up with detailed background questionnaire
- User profiles tracking software and hardware experience
- Secure authentication using Better Auth
- Profile management and preferences

### 2. **Personalized Learning**
- Content personalization based on user background
- Custom tips, exercises, and resources for each chapter
- Adaptive difficulty recommendations
- Hardware-specific or simulation-focused guidance

### 3. **Urdu Translation**
- One-click translation of entire chapters to Urdu
- Preserves code blocks and technical terms
- Toggle between English and Urdu
- Right-to-left text support

### 4. **RAG-Powered Chatbot**
- AI chatbot with context from course material
- Persistent chat history
- Accessible from any page

### 5. **Modern Documentation**
- Built with Docusaurus
- Responsive design
- Dark mode support
- Math equations with KaTeX
- Code syntax highlighting

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Setup Guides](#setup-guides)
- [Features Documentation](#features-documentation)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)

## Prerequisites

- **Node.js** 20+
- **Python** 3.9+ (for RAG chatbot)
- **npm** or **yarn**
- **Git**

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/tanveermurad/Physical-AI-Humanoid-Robotics-Course-Book.git
cd Physical-AI-Humanoid-Robotics-Course-Book
```

### 2. Start the Auth Server

Open a terminal:

```bash
cd auth-server
npm install --legacy-peer-deps
cp .env.example .env
# Edit .env and add a secure BETTER_AUTH_SECRET
npm run dev
```

The auth server will run on `http://localhost:3001`.

### 3. Start the RAG Chatbot API (Optional)

Open another terminal:

```bash
cd rag_chatbot_api
pip install -r requirements.txt
cp .env .env
# Configure your API keys in .env
python main.py
```

The chatbot API will run on `http://localhost:8000`.

### 4. Start the Frontend

Open another terminal:

```bash
cd my-book
npm install
npm start
```

The site will open at `http://localhost:3000`.

## Project Structure

```
Physical-AI-Humanoid-Robotics-Course-Book/
├── auth-server/              # Authentication server (Node.js + Better Auth)
│   ├── index.js              # Main server file
│   ├── package.json          # Dependencies
│   ├── .env                  # Environment variables
│   └── auth.db               # SQLite database (auto-created)
│
├── my-book/                  # Docusaurus frontend
│   ├── docs/                 # Course content (Markdown/MDX)
│   ├── src/
│   │   ├── components/
│   │   │   ├── AuthNav/      # Authentication navigation
│   │   │   ├── Chatbot/      # RAG chatbot UI
│   │   │   ├── PersonalizeChapter/  # Personalization component
│   │   │   └── TranslateChapter/    # Translation component
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx      # Global auth state
│   │   ├── lib/
│   │   │   └── auth-client.ts       # Better Auth client
│   │   ├── pages/
│   │   │   ├── signup.tsx           # Signup with questionnaire
│   │   │   ├── signin.tsx           # Sign in page
│   │   │   ├── profile.tsx          # User profile management
│   │   │   └── chatbot.tsx          # Chatbot page
│   │   ├── theme/
│   │   │   └── Root.tsx             # App wrapper with providers
│   │   └── types/
│   │       └── user.ts              # TypeScript types
│   ├── docusaurus.config.ts  # Docusaurus configuration
│   └── package.json
│
├── rag_chatbot_api/          # Python FastAPI backend
│   ├── main.py               # FastAPI app
│   ├── rag_core.py           # RAG logic
│   ├── database.py           # Chat history database
│   ├── models.py             # Pydantic models
│   └── requirements.txt      # Python dependencies
│
├── AUTHENTICATION_SETUP.md   # Auth setup guide
├── PERSONALIZATION_EXAMPLE.md # Personalization usage guide
├── TRANSLATION_GUIDE.md      # Translation feature guide
└── README.md                 # This file
```

## Setup Guides

### Detailed Setup Instructions

1. **[Authentication Setup Guide](AUTHENTICATION_SETUP.md)**
   - Complete guide to setting up Better Auth
   - User profile schema
   - API endpoints
   - Production deployment tips

2. **[Personalization Guide](PERSONALIZATION_EXAMPLE.md)**
   - How to add personalization to chapters
   - Personalization logic explained
   - Examples and best practices

3. **[Translation Guide](TRANSLATION_GUIDE.md)**
   - Adding Urdu translation to chapters
   - Translation API integration
   - Google/OpenAI/Microsoft translator setup
   - Pre-translation approach

## Features Documentation

### Authentication System

Built with [Better Auth](https://www.better-auth.com/), providing:
- Email/password authentication
- Session management
- User profiles with extended fields

**User Background Fields:**
- Programming experience (beginner to expert)
- Programming languages known
- AI/ML experience level
- ROS experience level
- Robotics experience (hobbyist to professional)
- Hardware projects completed
- Access to robotics hardware
- Learning goals
- Preferred content difficulty

### Personalization System

The `PersonalizeChapter` component provides:
- **Smart Tips**: Based on experience level and learning goals
- **Custom Exercises**: Matched to background and hardware availability
- **Resource Recommendations**: Tutorials and docs based on skill gaps
- **Difficulty Adaptation**: Beginner guides or advanced challenges

**Usage in MDX:**
```mdx
import PersonalizeChapter from '@site/src/components/PersonalizeChapter';

<PersonalizeChapter chapter="3" topic="ROS 2 Fundamentals" />
```

### Translation System

The `TranslateChapter` component enables:
- One-click Urdu translation
- Preserves code blocks and technical terms
- Toggle between languages
- RTL (right-to-left) text rendering

**Usage in MDX:**
```mdx
import TranslateChapter from '@site/src/components/TranslateChapter';

<TranslateChapter chapter="3" title="ROS 2 Architecture" />
```

### RAG Chatbot

An AI chatbot powered by:
- **Vector Database**: Qdrant for semantic search
- **Embeddings**: OpenAI or Google Gemini
- **LLM**: GPT-4 or Gemini for responses
- **Context**: Course material ingested from docs
- **History**: Persistent conversation history

**Features:**
- Answers questions about course content
- Provides code examples
- Remembers conversation context
- Accessible from any page

## Development

### Adding New Chapters

1. Create a new `.md` or `.mdx` file in `my-book/docs/`
2. Add frontmatter:
   ```mdx
   ---
   title: Your Chapter Title
   sidebar_position: 5
   ---
   ```
3. Add personalization and translation:
   ```mdx
   import PersonalizeChapter from '@site/src/components/PersonalizeChapter';
   import TranslateChapter from '@site/src/components/TranslateChapter';

   <TranslateChapter chapter="5" title="Your Chapter" />
   <PersonalizeChapter chapter="5" topic="Your Topic" />
   ```

### Updating RAG Content

To update the chatbot's knowledge base:

```bash
cd rag_chatbot_api
python ingest_data.py
```

This will re-index all documentation from `my-book/docs/`.

### Customizing User Profile Fields

Edit `auth-server/index.js` to add new fields:

```javascript
user: {
  additionalFields: {
    newField: {
      type: 'string',
      required: false,
    },
  },
}
```

Update TypeScript types in `my-book/src/types/user.ts`.

## Deployment

### Quick Deploy to GitHub Pages

The site is configured for automatic deployment to GitHub Pages:

```bash
# Commit and push to main branch
git add .
git commit -m "Deploy updates"
git push origin main
```

GitHub Actions will automatically:
1. Build the Docusaurus site
2. Deploy to GitHub Pages
3. Site goes live at: `https://tanveermurad.github.io/Physical-AI-Humanoid-Robotics-Course-Book/`

**Manual deployment:**
```bash
cd my-book
npm run build
npm run deploy
```

### Deploy Backend Services

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete instructions on deploying:
- Auth Server (Node.js) to Railway/Render
- Chatbot API (Python) to Railway/Render
- Environment configuration
- Production security setup

**Vercel/Netlify Alternative:**
- Connect your repository
- Build command: `cd my-book && npm run build`
- Output directory: `my-book/build`

### Auth Server

**Heroku:**
```bash
cd auth-server
heroku create your-app-name
git push heroku main
```

**Railway:**
```bash
railway init
railway up
```

Update `.env` variables in production:
- Use strong `BETTER_AUTH_SECRET`
- Set `BETTER_AUTH_URL` to your production URL
- Update `FRONTEND_URL` to your frontend domain
- Consider upgrading to PostgreSQL for database

### RAG Chatbot API

**Docker:**
```bash
cd rag_chatbot_api
docker build -t rag-chatbot .
docker run -p 8000:8000 rag-chatbot
```

**Railway/Render:**
- Connect repository
- Set environment variables
- Deploy `rag_chatbot_api` directory

## Environment Variables

### Auth Server (`.env`)
```env
BETTER_AUTH_SECRET=your-secure-secret
BETTER_AUTH_URL=http://localhost:3001
DATABASE_URL=./auth.db
FRONTEND_URL=http://localhost:3000
PORT=3001
```

### RAG Chatbot API (`.env`)
```env
DATABASE_URL=sqlite:///./chat_history.db
OPENAI_API_KEY=your-openai-key
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=optional-key
COLLECTION_NAME=robotics_docs
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4-turbo-preview
```

### Frontend
Environment variables are set in `docusaurus.config.ts`:
```typescript
webpack: {
  configureWebpack: (config) => {
    config.plugins.push(
      new webpack.DefinePlugin({
        'process.env.FRONTEND_API_BASE_URL': JSON.stringify('http://localhost:8000'),
      })
    );
  },
},
```

## Testing

### Testing Authentication

1. Navigate to `http://localhost:3000/signup`
2. Complete the 4-step questionnaire
3. Verify you're logged in (name appears in navbar)
4. Go to profile page to verify data saved correctly

### Testing Personalization

1. Log in with different user profiles
2. Navigate to a chapter with `<PersonalizeChapter />`
3. Click "Personalize This Chapter"
4. Verify tips/exercises match your profile

### Testing Translation

1. Log in
2. Navigate to a chapter with `<TranslateChapter />`
3. Click "Translate to Urdu"
4. Verify content is translated (currently placeholder)
5. Click "Show English" to toggle back

### Testing Chatbot

1. Open chatbot (bottom-right corner or `/chatbot`)
2. Ask a question about the course
3. Verify it responds with relevant content
4. Check conversation history persists

## Technologies Used

### Frontend
- **Docusaurus** 3.9 - Static site generator
- **React** 19 - UI library
- **TypeScript** - Type safety
- **Better Auth React** - Authentication client

### Backend (Auth)
- **Node.js** - Runtime
- **Express** - Web framework
- **Better Auth** - Authentication library
- **SQLite** - Database (dev) / PostgreSQL (prod)

### Backend (Chatbot)
- **Python** 3.9+
- **FastAPI** - Web framework
- **LangChain** - LLM orchestration
- **Qdrant** - Vector database
- **OpenAI** - Embeddings and LLM
- **SQLAlchemy** - Database ORM

## Troubleshooting

### Common Issues

**Issue: npm install fails with SSL errors**
Solution:
```bash
npm cache clean --force
npm install --legacy-peer-deps
```

**Issue: Auth server won't start**
Solution: Ensure `.env` file exists and `BETTER_AUTH_SECRET` is set

**Issue: Translation doesn't work**
Solution: Verify auth server is running and user is logged in

**Issue: Chatbot gives generic responses**
Solution: Run `python ingest_data.py` to index documentation

**Issue: TypeScript errors**
Solution:
```bash
cd my-book
npm install --save-dev @types/react @types/react-dom
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues or questions:
- Open a GitHub issue
- Check the [Authentication Setup Guide](AUTHENTICATION_SETUP.md)
- Check the [Translation Guide](TRANSLATION_GUIDE.md)
- Check the [Personalization Guide](PERSONALIZATION_EXAMPLE.md)

## Acknowledgments

- [Better Auth](https://www.better-auth.com/) for authentication
- [Docusaurus](https://docusaurus.io/) for the static site generator
- [LangChain](https://www.langchain.com/) for RAG implementation
- [Qdrant](https://qdrant.tech/) for vector search

---

**Built with ❤️ for the Panaversity Hackathon**

**Course Author**: Tanveer Murad
**Repository**: https://github.com/tanveermurad/Physical-AI-Humanoid-Robotics-Course-Book
