# 🚀 Automated Deployment Scripts

Complete deployment automation for your Physical AI course platform!

---

## 📋 What These Scripts Do

These scripts will **automatically**:
1. ✅ Deploy backend services to Render.com
2. ✅ Update frontend to use deployed URLs
3. ✅ Commit and push changes to GitHub
4. ✅ Verify everything is working

**Total time: ~15 minutes** (mostly waiting for deployments)

---

## 🎯 Quick Start (3 Steps)

### Step 1: Get Your Credentials (10 minutes)

You need accounts on 5 free services:

#### 1. Render.com (Hosting)
1. Go to: https://render.com
2. Sign up with GitHub
3. Go to: https://dashboard.render.com/u/settings#api-keys
4. Click "Create API Key"
5. Copy the key

#### 2. Neon (Database)
1. Go to: https://neon.tech
2. Sign up with GitHub
3. Create Project → Name: `physical-ai`
4. Copy "Connection String" (looks like: `postgresql://user:pass@...`)

#### 3. Qdrant Cloud (Vector Database)
1. Go to: https://cloud.qdrant.io
2. Sign up (free)
3. Create Cluster → Free Tier
4. Copy "Cluster URL" (looks like: `https://xxx.cloud.qdrant.io`)
5. Go to API Keys → Create → Copy the key

#### 4. OpenAI (AI)
1. Go to: https://platform.openai.com/api-keys
2. Sign up / Login
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-...`)

#### 5. GitHub Token (For pushing updates)
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: `deployment-script`
4. Select scope: `repo` (full control)
5. Click "Generate token"
6. Copy the token

---

### Step 2: Configure Credentials (2 minutes)

1. **Copy the example file:**
   ```bash
   cd deployment
   cp .env.example .env
   ```

2. **Edit `.env` file** and paste your credentials:
   ```bash
   # Open in your favorite editor
   notepad .env  # Windows
   # or
   nano .env     # Linux/Mac
   ```

3. **Fill in all values:**
   ```env
   RENDER_API_KEY=your_render_api_key_here
   NEON_DATABASE_URL=postgresql://user:pass@...
   QDRANT_URL=https://xxx.cloud.qdrant.io
   QDRANT_API_KEY=your_qdrant_key_here
   OPENAI_API_KEY=sk-proj-xxxxx
   GITHUB_TOKEN=ghp_xxxxx
   ```

4. **Save the file**

✅ **Credentials configured!**

---

### Step 3: Run Deployment (1 command!)

1. **Install Python dependencies:**
   ```bash
   cd deployment
   pip install -r requirements.txt
   ```

2. **Run the master deployment script:**
   ```bash
   python deploy_all.py
   ```

3. **Sit back and watch!** The script will:
   - ✅ Deploy auth server to Render
   - ✅ Deploy chatbot API to Render
   - ✅ Update frontend URLs
   - ✅ Push changes to GitHub
   - ✅ Verify everything works

4. **Wait ~15 minutes** for completion

✅ **Deployment complete!**

---

## 📁 What Each Script Does

### `deploy_all.py` (Master Script)
**Use this one!** Runs everything in order.

```bash
python deployment/deploy_all.py
```

Orchestrates the entire deployment process.

---

### `deploy_render.py` (Backend Deployment)
Deploys auth-server and chatbot-api to Render.com

```bash
python deployment/deploy_render.py
```

**What it does:**
- Creates 2 web services on Render
- Configures environment variables
- Waits for deployment to complete
- Saves deployment URLs to `deployment_info.json`

---

### `update_frontend.py` (Frontend URLs)
Updates frontend to use production backend URLs

```bash
python deployment/update_frontend.py
```

**What it does:**
- Reads `deployment_info.json`
- Updates `my-book/src/lib/auth-client.ts`
- Updates `my-book/src/components/Chatbot/index.tsx`
- Commits and pushes to GitHub

---

### `verify_deployment.py` (Testing)
Tests all services to ensure they're working

```bash
python deployment/verify_deployment.py
```

**What it does:**
- Tests auth server endpoints
- Tests chatbot API endpoints
- Tests frontend site
- Shows test summary

---

## 🔧 Manual Deployment (If Scripts Fail)

### Option 1: Use Individual Scripts

```bash
# Step 1: Deploy backends
python deployment/deploy_render.py

# Wait 5 minutes...

# Step 2: Update frontend
python deployment/update_frontend.py

# Wait 3 minutes...

# Step 3: Verify
python deployment/verify_deployment.py
```

---

### Option 2: Manual Render Deployment

If the scripts don't work, you can deploy manually:

1. **Go to Render Dashboard:**
   https://dashboard.render.com

2. **Deploy Auth Server:**
   - Click "New +" → "Web Service"
   - Connect GitHub repo
   - Settings:
     ```
     Name: physical-ai-auth-server
     Root Directory: auth-server
     Build: npm install --legacy-peer-deps
     Start: node index.js
     Plan: Free
     ```
   - Add environment variables from `.env`
   - Click "Create"

3. **Deploy Chatbot API:**
   - Click "New +" → "Web Service"
   - Connect GitHub repo
   - Settings:
     ```
     Name: physical-ai-chatbot-api
     Root Directory: rag_chatbot_api
     Build: pip install -r requirements.txt
     Start: python main.py
     Plan: Free
     ```
   - Add environment variables from `.env`
   - Click "Create"

4. **Update Frontend URLs:**
   - Edit `my-book/src/lib/auth-client.ts`
   - Edit `my-book/src/components/Chatbot/index.tsx`
   - Replace localhost URLs with Render URLs
   - Commit and push

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"
```bash
pip install -r deployment/requirements.txt
```

### "RENDER_API_KEY not found"
Make sure you created `deployment/.env` and filled in all credentials.

### "Git push failed"
Make sure your GitHub token has `repo` scope permissions.

### "Deployment timeout"
Render free tier can take 10-15 minutes to deploy. Be patient!

### "Services returning 503"
Services might be sleeping (Render free tier). Wait 60 seconds and try again.

### "CORS errors"
Backend services need to allow your frontend URL. Check environment variables.

---

## 💰 Cost Breakdown

| Service | Free Tier | Limit |
|---------|-----------|-------|
| **Render.com** | 750 hours/month per service | 2 services = FREE |
| **Neon Postgres** | 0.5GB, 100 compute hours | FREE |
| **Qdrant Cloud** | 1GB, 1M vectors | FREE |
| **OpenAI API** | $5 free credit | ~250 chats |
| **GitHub Pages** | Unlimited | FREE |

**Total: $0/month for testing!**

After $5 OpenAI credit: ~$0.02 per chat

---

## ⚠️ Important Notes

### Render Free Tier Limitations:
- Services **sleep after 15 minutes** of inactivity
- First request takes **30-60 seconds** to wake up
- This is **normal** and expected
- For production, upgrade to paid plan ($7/month per service)

### Security:
- ✅ `.env` is gitignored (credentials won't be committed)
- ✅ Use strong `BETTER_AUTH_SECRET` (auto-generated)
- ✅ Never commit credentials to GitHub

---

## 📊 Deployment Status Files

After running `deploy_render.py`, you'll get:

### `deployment_info.json`
```json
{
  "auth_server_url": "https://physical-ai-auth-server.onrender.com",
  "chatbot_api_url": "https://physical-ai-chatbot-api.onrender.com",
  "timestamp": "2025-01-15 10:30:00"
}
```

This file is used by other scripts to know your backend URLs.

---

## 🎉 Success Checklist

After running `deploy_all.py`, verify:

- [ ] No errors in script output
- [ ] `deployment_info.json` created with URLs
- [ ] Frontend files updated with production URLs
- [ ] Changes committed and pushed to GitHub
- [ ] Verification tests passed
- [ ] Site accessible at: https://tanveermurad.github.io/Physical-AI-Humanoid-Robotics-Course-Book/

**Test manually:**
- [ ] Sign up works
- [ ] Sign in works
- [ ] Chatbot responds (might take 60s first time)
- [ ] Personalization shows custom content
- [ ] Translation works

---

## 🔄 Redeploying After Changes

If you make changes to code:

```bash
# Commit your changes
git add .
git commit -m "Your changes"
git push origin main

# Render will auto-redeploy backend
# GitHub Actions will auto-redeploy frontend
# Wait 3-5 minutes
```

No need to run scripts again!

---

## 📞 Need Help?

1. **Check script output** - errors are usually descriptive
2. **Check Render dashboard** - view logs for backend services
3. **Run verify script** - `python deployment/verify_deployment.py`
4. **Check browser console** - F12 → Console for frontend errors

---

## 🎓 What You've Deployed

A complete AI-powered course platform with:

✅ **Frontend:**
- Static site on GitHub Pages
- Fast, free, unlimited bandwidth
- Auto-deploys on git push

✅ **Backend:**
- Node.js auth server (Better Auth)
- Python FastAPI chatbot (OpenAI Agents)
- Neon Postgres database
- Qdrant vector search

✅ **Features:**
- User authentication
- AI chatbot with course knowledge
- Text selection Q&A
- Personalized content
- Urdu translation
- Chat history
- Responsive design

**All deployed for FREE!** 🎉

---

## 📚 Additional Resources

- **Render Docs:** https://render.com/docs
- **Neon Docs:** https://neon.tech/docs
- **Qdrant Docs:** https://qdrant.tech/documentation
- **GitHub Pages:** https://pages.github.com

---

**Ready to deploy? Run:**
```bash
python deployment/deploy_all.py
```

🚀 **Good luck!**
