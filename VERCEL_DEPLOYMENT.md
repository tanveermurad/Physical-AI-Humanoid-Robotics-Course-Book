# Deploying to Vercel

This guide walks you through deploying the Physical AI & Humanoid Robotics Course Book to Vercel.

## Prerequisites

- A [Vercel account](https://vercel.com/signup) (free tier works fine)
- Your repository pushed to GitHub, GitLab, or Bitbucket
- Git installed locally

## Deployment Options

### Option 1: Deploy via Vercel Dashboard (Recommended)

This is the easiest method for first-time deployment.

#### Step 1: Import Your Repository

1. Go to [https://vercel.com/new](https://vercel.com/new)
2. Click "Import Git Repository"
3. Select your repository: `Physical-AI-Humanoid-Robotics-Course-Book`
4. Click "Import"

#### Step 2: Configure Project Settings

Vercel should auto-detect the settings, but verify:

- **Framework Preset**: Other (or None)
- **Root Directory**: `./` (leave as root)
- **Build Command**: `cd my-book && npm install && npm run build`
- **Output Directory**: `my-book/build`
- **Install Command**: `npm install --prefix my-book`

#### Step 3: Environment Variables (Optional)

If your frontend needs environment variables (like API URLs for auth server or chatbot):

1. Click "Environment Variables"
2. Add any required variables:
   - `REACT_APP_AUTH_SERVER_URL` (if needed)
   - `REACT_APP_CHATBOT_API_URL` (if needed)

#### Step 4: Deploy

1. Click "Deploy"
2. Wait for the build to complete (usually 2-5 minutes)
3. Your site will be live at `https://your-project-name.vercel.app`

### Option 2: Deploy via Vercel CLI

If you prefer command-line deployment:

#### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

#### Step 2: Login to Vercel

```bash
vercel login
```

#### Step 3: Deploy from Project Root

```bash
# Navigate to project root
cd Physical-AI-Humanoid-Robotics-Course-Book

# Deploy
vercel
```

Follow the prompts:
- Set up and deploy? **Yes**
- Which scope? Select your account
- Link to existing project? **No** (for first deployment)
- What's your project's name? Enter a name or press Enter
- In which directory is your code located? `./`

#### Step 4: Production Deployment

```bash
vercel --prod
```

## Configuration Files

The repository includes a `vercel.json` configuration file with the following settings:

```json
{
  "buildCommand": "cd my-book && npm install && npm run build",
  "outputDirectory": "my-book/build",
  "installCommand": "npm install --prefix my-book",
  "framework": null,
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

This configuration:
- Builds the Docusaurus site in the `my-book` directory
- Outputs static files to `my-book/build`
- Handles client-side routing with rewrites

## Post-Deployment Steps

### 1. Update Base URL (If Using Custom Domain)

If you're using a custom domain, update `my-book/docusaurus.config.ts`:

```typescript
url: 'https://your-custom-domain.com',
baseUrl: '/',
```

### 2. Configure Backend Services

The frontend needs to connect to backend services:

#### Auth Server
Deploy the auth server separately (see options below) and update the auth client configuration in `my-book/src/lib/auth-client.ts`:

```typescript
export const authClient = createAuthClient({
  baseURL: "https://your-auth-server.com"
});
```

#### RAG Chatbot API
Deploy the Python chatbot API separately and update the API URL in your chatbot component.

### 3. Set Up Custom Domain (Optional)

1. Go to your Vercel project dashboard
2. Click "Settings" > "Domains"
3. Add your custom domain
4. Follow Vercel's DNS configuration instructions

## Deploying Backend Services

The Docusaurus frontend is now on Vercel, but you still need to deploy the backend services:

### Auth Server (Node.js)

**Recommended Platforms:**
- **Render**: Easy deployment, free tier available
- **Railway**: Simple setup, generous free tier
- **Heroku**: Classic choice (paid)

**Quick Deploy to Render:**
1. Go to [https://render.com](https://render.com)
2. Create a new "Web Service"
3. Connect your repository
4. Set root directory to `auth-server`
5. Build command: `npm install`
6. Start command: `node index.js`
7. Add environment variables:
   - `BETTER_AUTH_SECRET`: Generate a secure secret
   - `BETTER_AUTH_URL`: Your Render service URL
   - `FRONTEND_URL`: Your Vercel URL
   - `DATABASE_URL`: Use Render PostgreSQL addon

### RAG Chatbot API (Python)

**Recommended Platforms:**
- **Render**: Good Python support
- **Railway**: Simple deployment
- **Fly.io**: Global edge deployment

**Quick Deploy to Render:**
1. Create a new "Web Service"
2. Connect your repository
3. Set root directory to `rag_chatbot_api`
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `QDRANT_URL`: Qdrant cloud or self-hosted URL
   - `DATABASE_URL`: PostgreSQL connection string

## Automatic Deployments

Vercel automatically deploys:
- **Production**: When you push to `main` branch
- **Preview**: For every pull request and branch push

You can view all deployments in your Vercel dashboard.

## Troubleshooting

### Build Fails

**Error: "Command failed: cd my-book && npm install && npm run build"**

Solution: Check the build logs for specific errors. Common issues:
- Missing dependencies
- TypeScript errors
- Node version mismatch

### Routes Not Working (404 Errors)

**Issue**: Navigating to routes like `/docs/intro` returns 404

Solution: This should be handled by the `rewrites` in `vercel.json`. If issues persist, add a `vercel.json` in the `my-book` directory:

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

### Docusaurus Assets Not Loading

**Issue**: CSS/JS files return 404

Solution: Verify `baseUrl` in `docusaurus.config.ts` is correct:
- For Vercel subdomain: `baseUrl: '/'`
- For custom domain: `baseUrl: '/'`
- For GitHub Pages: `baseUrl: '/Physical-AI-Humanoid-Robotics-Course-Book/'`

### Backend API Connection Issues

**Issue**: Auth or chatbot features don't work

Solution:
1. Verify backend services are deployed and running
2. Check environment variables in Vercel dashboard
3. Update API URLs in frontend code
4. Configure CORS on backend to allow Vercel domain

## Performance Optimization

### Enable Edge Network

Vercel automatically serves your site from their global CDN. No additional configuration needed.

### Image Optimization

If you add images, use Docusaurus's image handling:

```jsx
import useBaseUrl from '@docusaurus/useBaseUrl';

<img src={useBaseUrl('/img/my-image.png')} alt="Description" />
```

### Bundle Analysis

Add to `my-book/package.json`:

```json
"scripts": {
  "analyze": "ANALYZE=true npm run build"
}
```

Then run locally:
```bash
npm run analyze
```

## Monitoring

### Analytics

Add Vercel Analytics to track page views:

1. Go to your project dashboard
2. Click "Analytics" tab
3. Enable Vercel Analytics (free tier: 100K events/month)

### Logs

View deployment and runtime logs:
1. Go to your project dashboard
2. Click "Deployments"
3. Select a deployment
4. Click "View Function Logs"

## Rolling Back Deployments

If a deployment has issues:

1. Go to "Deployments" in Vercel dashboard
2. Find a previous working deployment
3. Click "..." menu
4. Select "Promote to Production"

## Environment-Specific Configurations

### Development vs Production

Create different configurations:

```typescript
// my-book/docusaurus.config.ts
const isDev = process.env.NODE_ENV === 'development';

const config: Config = {
  url: isDev
    ? 'http://localhost:3000'
    : 'https://your-vercel-domain.vercel.app',
  // ... rest of config
};
```

## Security Best Practices

1. Never commit `.env` files
2. Use Vercel's environment variables for secrets
3. Enable "Only Production" for sensitive environment variables
4. Use environment-specific API keys
5. Configure CORS properly on backend services

## Cost Considerations

Vercel Free Tier includes:
- 100GB bandwidth/month
- Unlimited deployments
- Automatic HTTPS
- DDoS protection
- Global CDN

For most course books, the free tier is sufficient. Monitor usage in the dashboard.

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Docusaurus Deployment Guide](https://docusaurus.io/docs/deployment)
- [Vercel CLI Reference](https://vercel.com/docs/cli)

## Support

If you encounter issues:
1. Check [Vercel Status](https://www.vercel-status.com/)
2. Review build logs in Vercel dashboard
3. Check [Vercel Community](https://github.com/vercel/vercel/discussions)
4. Open an issue in this repository

---

**Built for Panaversity Hackathon**
**Course Book by Tanveer Murad**
