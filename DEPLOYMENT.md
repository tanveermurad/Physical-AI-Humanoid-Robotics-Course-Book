# Deployment Guide

Complete guide for deploying the Physical AI & Humanoid Robotics Course Book to production.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│               Frontend (GitHub Pages)                        │
│  • Docusaurus static site                                    │
│  • Authentication UI                                          │
│  • Chatbot component                                          │
│  • Personalization components                                │
│  URL: https://tanveermurad.github.io/...                    │
└────────────┬────────────────────────────────────────────────┘
             │
             ├─────────────────────────────────────────────────┐
             │                                                  │
             ▼                                                  ▼
┌──────────────────────────────┐      ┌──────────────────────────────┐
│   Auth Server (Node.js)      │      │   Chatbot API (Python)       │
│   • Better Auth              │      │   • OpenAI Agents            │
│   • User profiles            │      │   • Qdrant Cloud             │
│   • Translation API          │      │   • Neon Postgres            │
│   Deploy: Railway/Render     │      │   Deploy: Railway/Render     │
│   Port: 3001                 │      │   Port: 8000                 │
└──────────────────────────────┘      └──────────────────────────────┘
```

## 📋 Prerequisites

- GitHub account with repo access
- Railway account (or Render/Heroku)
- Neon Postgres database (already set up)
- OpenAI API key
- Qdrant Cloud (already set up)

## 🚀 Part 1: Deploy Frontend to GitHub Pages

### Option A: Automatic Deployment (Recommended)

The repository is already configured with GitHub Actions for automatic deployment.

#### Step 1: Enable GitHub Pages

1. Go to your GitHub repository
2. Click **Settings** → **Pages**
3. Under **Source**, select:
   - **Branch**: `gh-pages`
   - **Folder**: `/ (root)`
4. Click **Save**

#### Step 2: Push to Main Branch

Every push to `main` branch will automatically trigger deployment:

```bash
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main
```

#### Step 3: Monitor Deployment

1. Go to **Actions** tab in GitHub
2. Watch the "Deploy to GitHub Pages" workflow
3. Once complete, site is live at:
   ```
   https://tanveermurad.github.io/Physical-AI-Humanoid-Robotics-Course-Book/
   ```

### Option B: Manual Deployment

```bash
cd my-book

# Set git user (if not already set)
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"

# Build and deploy
npm run build
npm run deploy
```

This will:
1. Build the site
2. Push to `gh-pages` branch
3. Deploy to GitHub Pages

### Verify Deployment

Visit: `https://tanveermurad.github.io/Physical-AI-Humanoid-Robotics-Course-Book/`

You should see your course book live!

## 🔧 Part 2: Deploy Backend Services

### Deploy Auth Server (Node.js) to Railway

#### Step 1: Sign Up for Railway

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Authorize Railway to access your repos

#### Step 2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository
4. Select **"auth-server"** directory

#### Step 3: Configure Environment Variables

In Railway project settings, add:

```env
BETTER_AUTH_SECRET=<your-secure-random-string>
BETTER_AUTH_URL=https://your-auth-server.railway.app
DATABASE_URL=<your-neon-connection-string>
FRONTEND_URL=https://tanveermurad.github.io
PORT=3001
NODE_ENV=production
```

#### Step 4: Deploy

Railway will automatically:
1. Detect Node.js project
2. Install dependencies
3. Start the server
4. Provide a URL: `https://your-project.railway.app`

#### Step 5: Update Frontend Environment

Update GitHub Actions workflow (`.github/workflows/deploy.yml`):

```yaml
- name: Build website
  run: npm run build
  env:
    FRONTEND_API_BASE_URL: https://your-chatbot-api.railway.app
```

Also update `my-book/docusaurus.config.ts`:

```typescript
webpack: {
  configureWebpack: (config: any) => {
    config.plugins.push(
      new (require('webpack').DefinePlugin)({
        'process.env.FRONTEND_API_BASE_URL': JSON.stringify(
          process.env.FRONTEND_API_BASE_URL ||
          'https://your-chatbot-api.railway.app'
        ),
      }),
    );
  },
},
```

### Deploy Chatbot API (Python) to Railway

#### Step 1: Create Another Railway Project

1. Click **"New Project"** again
2. Select **"Deploy from GitHub repo"**
3. Choose your repository
4. Select **"rag_chatbot_api"** directory

#### Step 2: Configure Environment Variables

In Railway project settings, add:

```env
# OpenAI
OPENAI_API_KEY=sk-proj-...

# Neon Postgres
DATABASE_URL=postgresql+asyncpg://user:pass@host.neon.tech/db?sslmode=require

# Qdrant Cloud
QDRANT_API_KEY=<your-qdrant-key>
QDRANT_HOST=https://your-cluster.aws.cloud.qdrant.io:6333
QDRANT_COLLECTION_NAME=book_content

# Google API (if using Gemini)
GOOGLE_API_KEY=<your-google-key>

# Configuration
EMBEDDING_MODEL_NAME=gemini
LLM_MODEL_NAME=gemini
PORT=8000
```

#### Step 3: Create railway.json

Railway needs to know how to start your Python app:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### Step 4: Deploy

Railway will:
1. Detect Python project
2. Install requirements.txt
3. Start FastAPI server
4. Provide URL: `https://your-chatbot.railway.app`

#### Step 5: Update CORS Settings

In `rag_chatbot_api/main.py`, update CORS origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tanveermurad.github.io",  # Your GitHub Pages domain
        "http://localhost:3000",  # Keep for local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Alternative: Deploy to Render

#### Auth Server on Render

1. Go to [render.com](https://render.com)
2. Create **New Web Service**
3. Connect GitHub repo
4. Settings:
   - **Name**: `physical-ai-auth`
   - **Root Directory**: `auth-server`
   - **Environment**: `Node`
   - **Build Command**: `npm install`
   - **Start Command**: `node index.js`
5. Add environment variables (same as Railway)
6. Click **Create Web Service**

#### Chatbot API on Render

1. Create **New Web Service**
2. Connect GitHub repo
3. Settings:
   - **Name**: `physical-ai-chatbot`
   - **Root Directory**: `rag_chatbot_api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables
5. Click **Create Web Service**

## 🔐 Part 3: Security Configuration

### Update Auth Server CORS

In `auth-server/index.js`:

```javascript
app.use(cors({
  origin: 'https://tanveermurad.github.io',
  credentials: true,
}));

export const auth = betterAuth({
  // ... existing config
  trustedOrigins: [
    'https://tanveermurad.github.io',
  ],
});
```

### Generate Secure Secrets

For production `BETTER_AUTH_SECRET`:

```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

Copy the output and use it as your `BETTER_AUTH_SECRET` in Railway/Render.

### Update Frontend API URLs

Create `my-book/.env.production`:

```env
FRONTEND_API_BASE_URL=https://your-chatbot-api.railway.app
```

## 📊 Part 4: Database Setup (Neon)

Your Neon database is already set up! But for production:

### Verify Connection String

Ensure your `DATABASE_URL` includes `?sslmode=require`:

```
postgresql+asyncpg://user:pass@host.neon.tech/db?sslmode=require
```

### Monitor Usage

1. Go to [Neon Console](https://console.neon.tech)
2. Check **Storage** and **Compute** usage
3. Free tier limits:
   - 0.5 GB storage
   - 100 hours compute/month

### Upgrade if Needed

If you exceed free tier:
- **Launch Plan**: $19/month
- **Scale Plan**: $69/month
- Only pay for what you use beyond free tier

## 🧪 Part 5: Testing Production Deployment

### Test Checklist

#### Frontend Tests

- [ ] Site loads at GitHub Pages URL
- [ ] Navigation works (all pages load)
- [ ] Dark mode toggle works
- [ ] Mobile responsive
- [ ] Math equations render (KaTeX)
- [ ] Code highlighting works

#### Authentication Tests

- [ ] Can sign up (4-step form works)
- [ ] Can sign in
- [ ] Profile page loads
- [ ] Profile editing works
- [ ] Sign out works
- [ ] Auth persists across page reloads

#### Chatbot Tests

- [ ] Chatbot opens/closes
- [ ] Can send messages
- [ ] Receives responses from OpenAI
- [ ] Sources are displayed
- [ ] Text selection works:
  - Select text from chapter
  - Open chatbot
  - Selected text banner appears
  - Response references selection
- [ ] Personalization works:
  - Sign in
  - Set profile (beginner/advanced)
  - Verify response style adapts
- [ ] Chat history persists in Neon

#### Translation Tests

- [ ] Translation button appears
- [ ] Click translates to Urdu
- [ ] Toggle back to English works

#### Personalization Tests

- [ ] "Personalize This Chapter" button works
- [ ] Shows relevant tips based on profile
- [ ] Recommendations match user level

### Monitor Errors

#### Frontend Errors

Check browser console (F12):
```javascript
// Should see no CORS errors
// Should see successful API calls
```

#### Backend Errors

Check Railway/Render logs:
```bash
# In Railway dashboard
Click on deployment → View Logs
```

Look for:
- Successful database connections
- No OpenAI API errors
- No Qdrant connection errors

## 💰 Cost Breakdown

### Free Tier Usage

**GitHub Pages**: FREE ✅
- Unlimited public repos
- Unlimited bandwidth
- Custom domain support

**Railway Free Trial**: $5 credit
- Lasts ~1 month for low traffic
- Then $5/month per service

**Neon Postgres**: FREE ✅
- 0.5 GB storage
- 100 compute hours/month
- Auto-pauses when idle

**Qdrant Cloud**: FREE ✅
- 1 GB storage
- 1M vectors
- Already configured!

**OpenAI API**: Pay-as-you-go
- ~$0.02 per query (GPT-4 Turbo)
- 100 queries = $2
- 1000 queries = $20

### Monthly Cost Estimate

**Low Traffic** (100 users, 10 queries/day):
- Frontend: FREE
- Railway: $10 (both services)
- Neon: FREE
- Qdrant: FREE
- OpenAI: ~$60
- **Total: ~$70/month**

**Medium Traffic** (500 users, 30 queries/day):
- Frontend: FREE
- Railway: $10
- Neon: FREE (might need upgrade)
- Qdrant: FREE
- OpenAI: ~$600
- **Total: ~$610/month**

## 🔄 Continuous Deployment

### Automatic Updates

With GitHub Actions configured, every push to `main` triggers:

1. **Build** - Docusaurus builds static site
2. **Test** - (add tests in workflow if needed)
3. **Deploy** - Push to gh-pages branch
4. **Live** - GitHub Pages serves new version

### Manual Backend Updates

Railway/Render automatically redeploy on git push:

```bash
# Make changes to auth-server or rag_chatbot_api
git add .
git commit -m "Update backend"
git push origin main
```

Railway/Render detect changes and redeploy.

### Environment-Specific Builds

Development:
```bash
cd my-book
npm start  # Uses localhost:8000 for API
```

Production (automatic via GitHub Actions):
```bash
FRONTEND_API_BASE_URL=https://prod-api.railway.app npm run build
```

## 🐛 Troubleshooting Deployment

### Issue: GitHub Pages shows 404

**Solution:**
1. Check `gh-pages` branch exists
2. Verify GitHub Pages settings point to `gh-pages` branch
3. Wait 5-10 minutes after first deployment

### Issue: "Broken link" errors during build

**Solution:**
Check `onBrokenLinks: 'throw'` in docusaurus.config.ts.
Temporarily set to `'warn'` during development:

```typescript
onBrokenLinks: 'warn',
```

### Issue: CORS errors in production

**Solution:**
1. Check auth-server CORS includes GitHub Pages URL
2. Check chatbot API CORS includes GitHub Pages URL
3. Verify `credentials: 'include'` in fetch requests

### Issue: Environment variables not working

**Railway:**
1. Go to project → Variables
2. Click "Raw Editor"
3. Paste all variables
4. Click "Deploy"

**Render:**
1. Go to service → Environment
2. Add each variable manually
3. Click "Save Changes"

### Issue: Database connection fails

**Check:**
1. Neon project not paused (free tier auto-pauses)
2. Connection string includes `?sslmode=require`
3. Railway/Render has correct `DATABASE_URL`

### Issue: OpenAI API rate limits

**Solution:**
1. Check OpenAI dashboard for usage
2. Add rate limiting in `main.py`:
   ```python
   from slowapi import Limiter

   limiter = Limiter(key_func=lambda: request.client.host)

   @app.post("/chat")
   @limiter.limit("10/minute")
   async def chat(...):
       ...
   ```

## 📈 Monitoring & Analytics

### Add Google Analytics (Optional)

In `my-book/docusaurus.config.ts`:

```typescript
themeConfig: {
  // ... existing config
  gtag: {
    trackingID: 'G-XXXXXXXXXX',
    anonymizeIP: true,
  },
},
```

### Monitor Backend Health

**Railway Dashboard:**
- CPU usage
- Memory usage
- Request count
- Error logs

**Neon Dashboard:**
- Storage used
- Compute hours
- Query performance

**OpenAI Dashboard:**
- API usage
- Token consumption
- Cost tracking

## 🎯 Next Steps After Deployment

1. **Test thoroughly** using the checklist above
2. **Monitor costs** in first week
3. **Set up alerts** for unusual traffic
4. **Add analytics** to track user behavior
5. **Collect feedback** from users
6. **Iterate** based on usage patterns

## 📚 Quick Commands Reference

```bash
# Frontend deployment (automatic)
git push origin main

# Frontend deployment (manual)
cd my-book
npm run deploy

# Check deployment status
git log gh-pages --oneline

# View production site
open https://tanveermurad.github.io/Physical-AI-Humanoid-Robotics-Course-Book/

# Monitor backend logs (Railway CLI)
railway logs -s auth-server
railway logs -s chatbot-api

# Test production API
curl https://your-api.railway.app/health
```

## 🆘 Getting Help

- **GitHub Pages Issues**: [GitHub Docs](https://docs.github.com/en/pages)
- **Railway Support**: [Railway Docs](https://docs.railway.app)
- **Render Support**: [Render Docs](https://render.com/docs)
- **Docusaurus Issues**: [Docusaurus Docs](https://docusaurus.io/docs/deployment)

---

**Deployment complete!** Your course book is now live and accessible worldwide! 🌍
