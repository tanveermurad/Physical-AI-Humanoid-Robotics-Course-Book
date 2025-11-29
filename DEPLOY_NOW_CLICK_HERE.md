# 🚀 DEPLOY IN 3 CLICKS

## YOUR WEBSITE IS ALREADY LIVE! ✅

Visit: https://tanveermurad.github.io/Physical-AI-Humanoid-Robotics-Course-Book/

But authentication and chatbot need backend servers. Here's how to deploy them:

---

## 🎯 METHOD 1: One-Click Deploy on Render (EASIEST)

### Step 1: Get Your Free Services (Required)

You MUST create these accounts first (all FREE):

#### A. Get Database (2 minutes)
1. **Click:** https://neon.tech
2. Click "Sign Up" → Use GitHub
3. Create Project → Name: `physical-ai`
4. Copy the **Connection String** (looks like: `postgresql://user:pass@...`)
5. **SAVE IT** - You'll need this!

#### B. Get Vector Database (2 minutes)
1. **Click:** https://cloud.qdrant.io
2. Sign up (free)
3. Create Cluster → Name: `robotics` → Free Tier
4. Copy **Cluster URL** (looks like: `https://xxx.cloud.qdrant.io`)
5. Go to API Keys → Create → Copy the key
6. **SAVE BOTH** - You'll need these!

#### C. Get OpenAI Key (2 minutes)
1. **Click:** https://platform.openai.com/api-keys
2. Sign up / Login
3. Click "Create new secret key"
4. Copy it (starts with `sk-proj-...`)
5. **SAVE IT** - You'll need this!

---

### Step 2: Deploy Backend (ONE CLICK!)

1. **Click this button:**

   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/tanveermurad/Physical-AI-Humanoid-Robotics-Course-Book)

2. **Sign up on Render** (use GitHub)

3. **Render will ask for environment variables. Paste:**
   - `DATABASE_URL` → Your Neon connection string
   - `QDRANT_URL` → Your Qdrant URL
   - `QDRANT_API_KEY` → Your Qdrant API key
   - `OPENAI_API_KEY` → Your OpenAI key
   - `BETTER_AUTH_URL` → Will be generated (you'll update this later)

4. **Click "Apply"**

5. **Wait 10 minutes** for deployment

---

### Step 3: Connect Frontend to Backend

After deployment, Render will give you 2 URLs:
- `https://physical-ai-auth-server.onrender.com`
- `https://physical-ai-chatbot-api.onrender.com`

**You need to update 2 files:**

#### File 1: `my-book/src/lib/auth-client.ts`

Go to: https://github.com/tanveermurad/Physical-AI-Humanoid-Robotics-Course-Book/blob/main/my-book/src/lib/auth-client.ts

Click Edit → Change line 4:
```typescript
baseURL: 'https://physical-ai-auth-server.onrender.com'  // YOUR URL
```

#### File 2: `my-book/src/components/Chatbot/index.tsx`

Go to: https://github.com/tanveermurad/Physical-AI-Humanoid-Robotics-Course-Book/blob/main/my-book/src/components/Chatbot/index.tsx

Click Edit → Change line ~10:
```typescript
const CHATBOT_API_URL = 'https://physical-ai-chatbot-api.onrender.com';  // YOUR URL
```

**Commit both changes!**

Wait 2 minutes → Your site will auto-deploy!

✅ **DONE!**

---

## 🎯 METHOD 2: Manual Render Deployment

If the button doesn't work:

### 1. Go to Render Dashboard
https://dashboard.render.com

### 2. Deploy Auth Server
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
- Add environment variables (from Step 1 above)
- Click "Create"

### 3. Deploy Chatbot API
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
- Add environment variables (from Step 1 above)
- Click "Create"

### 4. Update Frontend URLs
(Same as Method 1, Step 3)

---

## 🎯 METHOD 3: Railway (Alternative)

### 1. Get Free Services (Same as Method 1, Step 1)

### 2. Deploy on Railway

**Click:** https://railway.app

1. Sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will ask: "Which service?"
5. Select `auth-server` → Add environment variables → Deploy
6. Repeat for `rag_chatbot_api`

### 3. Update Frontend URLs (Same as Method 1, Step 3)

---

## 🆘 I DON'T HAVE TIME!

### Quick Test Version (No Deployment Needed)

Want to test locally first?

1. Open 3 terminals:

**Terminal 1 (Auth Server):**
```bash
cd auth-server
npm install --legacy-peer-deps
npm run dev
```

**Terminal 2 (Chatbot API):**
```bash
cd rag_chatbot_api
pip install -r requirements.txt
python main.py
```

**Terminal 3 (Frontend):**
```bash
cd my-book
npm start
```

Visit: http://localhost:3000

Test everything locally before deploying!

---

## ✅ Checklist

- [ ] Created Neon account (database)
- [ ] Created Qdrant account (vector DB)
- [ ] Got OpenAI API key
- [ ] Deployed auth-server on Render/Railway
- [ ] Deployed chatbot-api on Render/Railway
- [ ] Updated frontend URLs in GitHub
- [ ] Tested signup on live site
- [ ] Tested chatbot on live site

---

## 💰 Cost: $0/month (100% FREE!)

- GitHub Pages: FREE
- Render.com: FREE (2 services)
- Neon: FREE (0.5GB)
- Qdrant: FREE (1GB)
- OpenAI: $5 free credit (~250 chats)

**Total: FREE for learning/testing!**

---

## 🎉 After Deployment

Your site will have:
- ✅ User signup/login
- ✅ AI chatbot with course knowledge
- ✅ Text selection questions
- ✅ Personalized content
- ✅ Urdu translation
- ✅ Chat history saved
- ✅ All features working!

**Visit:** https://tanveermurad.github.io/Physical-AI-Humanoid-Robotics-Course-Book/

---

## 📞 Need Help?

Tell me where you're stuck:
- "I created accounts, now what?"
- "I'm on Render, what settings to use?"
- "I deployed but getting errors"
- "How do I update frontend URLs?"

I'll guide you step-by-step!
