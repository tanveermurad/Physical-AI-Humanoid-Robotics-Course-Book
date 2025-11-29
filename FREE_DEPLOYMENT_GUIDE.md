# 🆓 FREE Deployment Guide - Step by Step

Deploy your entire project for FREE in 30 minutes!

---

## ✅ Part 1: Frontend (Already Done!)

Your website frontend is already deploying to GitHub Pages for FREE!

**Check it here in 2-3 minutes:**
```
https://tanveermurad.github.io/Physical-AI-Humanoid-Robotics-Course-Book/
```

---

## 🔧 Part 2: Deploy Backend Services (FREE)

You need to deploy 2 backend services. I'll show you the EASIEST free option.

---

## Option A: Use Render.com (EASIEST & FREE)

### Step 1: Create Render Account (2 minutes)

1. Go to https://render.com
2. Click "Get Started"
3. Sign up with your GitHub account (click "GitHub" button)
4. Authorize Render to access your repositories

✅ **Done!** You're now logged into Render.

---

### Step 2: Deploy Auth Server (5 minutes)

1. **Click "New +" button** (top right)
2. **Select "Web Service"**
3. **Connect your repository:**
   - Find: `Physical-AI-Humanoid-Robotics-Course-Book`
   - Click "Connect"

4. **Configure the service:**
   ```
   Name: physical-ai-auth-server
   Region: Choose closest to you
   Branch: main
   Root Directory: auth-server
   Runtime: Node
   Build Command: npm install --legacy-peer-deps
   Start Command: node index.js
   Instance Type: Free
   ```

5. **Add Environment Variables** (click "Advanced" → "Add Environment Variable"):
   ```
   BETTER_AUTH_SECRET=your-secure-random-string-min-32-chars
   BETTER_AUTH_URL=https://physical-ai-auth-server.onrender.com
   FRONTEND_URL=https://tanveermurad.github.io
   PORT=3001
   ```

   **How to generate BETTER_AUTH_SECRET:**
   - Go to https://www.uuidgenerator.net/
   - Copy any UUID and repeat it 2 times
   - Example: `a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890`

6. **Click "Create Web Service"**

7. **Wait 3-5 minutes** for deployment

8. **Copy your URL** (looks like: `https://physical-ai-auth-server.onrender.com`)

✅ **Auth Server Deployed!**

---

### Step 3: Get Free Database (Neon Postgres) (3 minutes)

1. **Go to https://neon.tech**
2. **Sign up** with GitHub
3. **Create a project:**
   - Name: `physical-ai-chatbot`
   - Region: Choose closest to you
   - Click "Create Project"

4. **Copy the connection string:**
   - Click "Connection String"
   - Copy the string (looks like: `postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb`)

✅ **Database Ready!**

---

### Step 4: Get Free Vector Database (Qdrant Cloud) (3 minutes)

1. **Go to https://cloud.qdrant.io**
2. **Sign up** (free account)
3. **Create a cluster:**
   - Name: `robotics-docs`
   - Region: Choose closest to you
   - Plan: Free Tier (1GB)
   - Click "Create"

4. **Get API credentials:**
   - Click on your cluster
   - Copy "Cluster URL" (looks like: `https://xxx.aws.cloud.qdrant.io`)
   - Click "API Keys" → "Create"
   - Copy the API key

✅ **Vector Database Ready!**

---

### Step 5: Get OpenAI API Key (2 minutes)

1. **Go to https://platform.openai.com**
2. **Sign up / Log in**
3. **Add payment method** (required, but you get $5 free credit)
4. **Create API key:**
   - Go to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the key (starts with `sk-proj-...`)

✅ **OpenAI Key Ready!**

---

### Step 6: Deploy Chatbot API (5 minutes)

1. **Go back to Render.com**
2. **Click "New +" → "Web Service"**
3. **Connect your repository** again
4. **Configure:**
   ```
   Name: physical-ai-chatbot-api
   Region: Choose closest to you
   Branch: main
   Root Directory: rag_chatbot_api
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
   Instance Type: Free
   ```

5. **Add Environment Variables:**
   ```
   DATABASE_URL=<paste Neon connection string from Step 3>
   OPENAI_API_KEY=<paste OpenAI key from Step 5>
   QDRANT_URL=<paste Qdrant URL from Step 4>
   QDRANT_API_KEY=<paste Qdrant API key from Step 4>
   COLLECTION_NAME=robotics_docs
   EMBEDDING_MODEL=text-embedding-3-small
   LLM_MODEL=gpt-4-turbo-preview
   PORT=8000
   ```

6. **Click "Create Web Service"**

7. **Wait 5-10 minutes** for deployment

8. **Copy your URL** (looks like: `https://physical-ai-chatbot-api.onrender.com`)

✅ **Chatbot API Deployed!**

---

### Step 7: Update Frontend URLs (3 minutes)

Now you need to tell your frontend where the backend services are.

1. **Open GitHub** in browser
2. **Go to your repository:**
   ```
   https://github.com/tanveermurad/Physical-AI-Humanoid-Robotics-Course-Book
   ```

3. **Edit file: `my-book/src/lib/auth-client.ts`**
   - Click the file → Click pencil icon (Edit)
   - Find line with `baseURL: 'http://localhost:3001'`
   - Change to: `baseURL: 'https://physical-ai-auth-server.onrender.com'`
   - Click "Commit changes"

4. **Edit file: `my-book/src/components/Chatbot/index.tsx`**
   - Find: `const CHATBOT_API_URL = 'http://localhost:8000'`
   - Change to: `const CHATBOT_API_URL = 'https://physical-ai-chatbot-api.onrender.com'`
   - Click "Commit changes"

5. **Wait 2-3 minutes** - GitHub will automatically redeploy!

✅ **Everything Connected!**

---

## 🎉 Testing Your Deployment

### Test 1: Check if site is live
```
https://tanveermurad.github.io/Physical-AI-Humanoid-Robotics-Course-Book/
```

### Test 2: Check if auth server is running
```
https://physical-ai-auth-server.onrender.com/api/auth/session
```
Should show: `{"user":null,"session":null}`

### Test 3: Check if chatbot API is running
```
https://physical-ai-chatbot-api.onrender.com/health
```
Should show: `{"status":"healthy"}`

### Test 4: Try signing up
1. Go to your site
2. Click "Sign Up"
3. Fill the form
4. If it works, everything is deployed! ✅

---

## 💰 Total Cost: $0 / month

| Service | Plan | Cost |
|---------|------|------|
| GitHub Pages | Free | $0 |
| Render.com (Auth Server) | Free Tier | $0 |
| Render.com (Chatbot API) | Free Tier | $0 |
| Neon Postgres | Free Tier | $0 |
| Qdrant Cloud | Free Tier | $0 |
| OpenAI API | Pay-per-use | ~$0.02/chat (you get $5 free) |

**Total: FREE** (until you use up $5 OpenAI credit)

---

## ⚠️ Important Notes

### Render Free Tier Limitations:
- Services sleep after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- 750 hours/month free (enough for 1 service 24/7)

### Solution:
- For production, upgrade to Render paid plan ($7/month per service)
- Or use Railway.com (also has free tier)

---

## 🆘 Troubleshooting

### "Auth server not responding"
- Wait 60 seconds (it's waking up from sleep)
- Check Render dashboard for errors

### "Database connection failed"
- Verify Neon connection string is correct
- Check if Neon project is active

### "Chatbot not working"
- Check OpenAI API key is valid
- Verify you have credits in OpenAI account
- Check Qdrant credentials

### "CORS errors in browser"
- Add your GitHub Pages URL to CORS settings in both backend services
- Redeploy services

---

## 📞 Need Help?

1. Check Render logs: Dashboard → Your Service → Logs
2. Check browser console: F12 → Console tab
3. Open GitHub issue with error message

---

## 🚀 Your Project is LIVE!

Visit: https://tanveermurad.github.io/Physical-AI-Humanoid-Robotics-Course-Book/

**Congratulations! You've deployed a complete AI-powered course platform for FREE!** 🎉
