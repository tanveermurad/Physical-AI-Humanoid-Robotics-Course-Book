# 🚀 Deploy to GitHub Pages NOW

Quick guide to get your site live in 5 minutes!

## Step 1: Enable GitHub Pages (1 minute)

1. Go to your GitHub repository
2. Click **Settings** → **Pages** (left sidebar)
3. Under **Source**, select:
   - **Branch**: `gh-pages`
   - **Folder**: `/ (root)`
4. Click **Save**

## Step 2: Push to GitHub (2 minutes)

```bash
# Stage all changes
git add .

# Commit with message
git commit -m "Deploy to GitHub Pages with authentication and chatbot"

# Push to main branch
git push origin main
```

## Step 3: Watch Deployment (2 minutes)

1. Go to **Actions** tab in your GitHub repo
2. Click on the running "Deploy to GitHub Pages" workflow
3. Watch it build and deploy (takes ~2-3 minutes)
4. ✅ Once complete, green checkmark appears

## Step 4: Visit Your Live Site!

```
https://tanveermurad.github.io/Physical-AI-Humanoid-Robotics-Course-Book/
```

🎉 **Your course book is now LIVE!**

## What's Deployed

✅ **Frontend (GitHub Pages)**
- Complete Docusaurus site
- All course chapters
- Authentication pages (signup/signin/profile)
- Personalization components
- Translation components
- Chatbot UI

⚠️ **Backend Services** (need separate deployment)
- Auth Server (Node.js)
- Chatbot API (Python)

## Deploy Backend Services

The frontend is live, but authentication and chatbot need backend services.

### Quick Backend Deploy (Railway - 10 minutes)

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for step-by-step instructions on:

1. **Deploy Auth Server** (5 min)
   - Sign up at railway.app
   - Connect GitHub repo
   - Select `auth-server` folder
   - Add environment variables
   - Get URL: `https://your-auth.railway.app`

2. **Deploy Chatbot API** (5 min)
   - Create another Railway project
   - Select `rag_chatbot_api` folder
   - Add environment variables (OpenAI, Neon, Qdrant)
   - Get URL: `https://your-chatbot.railway.app`

3. **Update Frontend URLs**
   - Edit `.github/workflows/deploy.yml`
   - Add backend URLs to environment
   - Push to trigger redeployment

## Testing Your Deployment

### Without Backend (Works Now!)
- ✅ Browse all chapters
- ✅ Read course content
- ✅ View markdown formatting
- ✅ Code syntax highlighting
- ✅ Math equations
- ❌ Sign up/Sign in (needs auth server)
- ❌ Chatbot (needs chatbot API)

### With Backend (After Railway Deploy)
- ✅ Everything above PLUS:
- ✅ User authentication
- ✅ Personalized content
- ✅ Urdu translation
- ✅ AI chatbot with text selection

## Next Steps

1. **Test the live site**: Visit the URL above
2. **Deploy backend**: Follow [DEPLOYMENT.md](DEPLOYMENT.md)
3. **Update environment**: Configure production URLs
4. **Test full features**: Authentication + Chatbot
5. **Share with users**: Your course is live!

## Troubleshooting

### Site shows 404

Wait 5-10 minutes after first deployment. GitHub Pages needs time to provision.

### Deployment failed in Actions

Check the workflow log for errors. Common issues:
- Node version mismatch (should be 20)
- npm install errors (run `npm ci` locally first)
- Build errors (run `npm run build` locally first)

### Pages not enabled

Go to Settings → Pages and ensure `gh-pages` branch is selected.

## Manual Deploy Alternative

If automatic deployment doesn't work:

```bash
cd my-book

# Build the site
npm run build

# Deploy manually
npm run deploy
```

This will build and push to `gh-pages` branch directly.

## Update Your Site

Every time you push to main, your site automatically updates:

```bash
# Make changes to docs or code
# Then commit and push

git add .
git commit -m "Update course content"
git push origin main

# Wait 2-3 minutes for deployment
# Visit site to see changes
```

---

**Need help?** Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions or open a GitHub issue.

**Site URL**: https://tanveermurad.github.io/Physical-AI-Humanoid-Robotics-Course-Book/
