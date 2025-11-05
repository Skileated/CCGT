# CCGT Vercel Deployment Guide

This guide explains how to deploy the CCGT (Contextual Coherence Graph Transformer) web interface to Vercel. The frontend is built with React, Vite, and Tailwind CSS, and can optionally connect to a FastAPI backend hosted elsewhere.

## Overview

CCGT is a web application that evaluates textual coherence by analyzing semantic relationships and discourse flow between sentences. The frontend provides an intuitive interface for text analysis, visualization, and coherence scoring.

## Prerequisites

Before deploying, ensure you have:

- **Node.js** (v18 or higher)
- **npm** or **yarn** package manager
- **Vercel account** ([sign up here](https://vercel.com/signup))
- **GitHub repository** with your code (e.g., `https://github.com/Skileated/CCGT`)

## Project Structure

```
CCGT/
├── frontend/              # React + Vite + Tailwind app
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── backend/               # FastAPI coherence API
│   ├── app/
│   └── requirements.txt
├── requirements.txt
├── README.md
└── DEPLOYMENT_GUIDE.md
```

## Local Setup Instructions

First, verify that the frontend runs locally:

```bash
cd frontend
npm install
npm run dev
```

The application should be available at `http://localhost:5173/`. Test all features:

- Navigation (Home, Try Demo, Contact Us)
- Text evaluation functionality
- Graph visualizations
- Responsive layout

## Preparing for Vercel Deployment

### Step 1: Push Code to GitHub

Ensure your latest code is committed and pushed to your GitHub repository:

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 2: Create Vercel Project

1. Log into [Vercel](https://vercel.com/login)
2. Click **"New Project"**
3. Select **"Import Git Repository"**
4. Choose your GitHub repository
5. **Important**: In the project configuration, set:
   - **Root Directory**: `frontend`
   - **Framework Preset**: `Vite`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install` (default)

### Step 3: Configure Build Settings

In **Project Settings → Build & Output Settings**, verify:

- **Framework Preset**: Vite
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Node.js Version**: 18.x or higher

## Environment Variables

If your frontend connects to a FastAPI backend hosted elsewhere (e.g., Render, Railway, or your own server), configure the API URL:

1. Go to **Settings → Environment Variables** in Vercel
2. Add a new variable:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-backend-url.onrender.com` (or your backend URL)
   - **Environment**: Production, Preview, Development (select all)

**Note**: Environment variables prefixed with `VITE_` are exposed to the frontend bundle. Never include sensitive API keys here.

### Example

```
VITE_API_URL=https://ccgt-api.onrender.com
```

If no backend is configured, the frontend will default to `http://127.0.0.1:8000` for local development.

## Build and Deploy

Once configured, click **"Deploy"**. Vercel will automatically:

1. Install dependencies (`npm install`)
2. Build the project (`npm run build`)
3. Deploy to a public URL (e.g., `https://ccgt.vercel.app`)

The deployment typically takes 1-3 minutes. You'll receive a notification when it's complete.

### Automatic Deployments

Vercel automatically deploys:
- **Production**: Every push to your main branch
- **Preview**: Every pull request and push to other branches

## Verifying Deployment

After deployment, test the following:

### Navigation
- ✅ Home page loads with hero section
- ✅ "Try Demo" navigates to `/demo`
- ✅ "Contact Us" scrolls smoothly to contact form
- ✅ GitHub link opens correctly

### Functionality
- ✅ Text evaluation API call succeeds
- ✅ Coherence score displays correctly
- ✅ Graph visualization renders
- ✅ Sentence-level scores table appears
- ✅ Line graph displays coherence trend

### UI/UX
- ✅ Responsive layout on mobile devices
- ✅ Footer appears at bottom of all pages
- ✅ Animations and transitions work smoothly
- ✅ No console errors

## Optional: Backend Deployment

If deploying the FastAPI backend separately (e.g., on Render, Railway, or AWS), ensure CORS is enabled:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production Recommendation**: Replace `allow_origins=["*"]` with your specific Vercel domain:

```python
allow_origins=["https://ccgt.vercel.app", "https://ccgt-git-main.vercel.app"]
```

## Troubleshooting

### Blank Page on Load

**Issue**: The page loads but shows a blank screen.

**Solution**: 
1. Check `vite.config.js` for base path configuration
2. Verify `base: '/'` is set correctly
3. Check browser console for JavaScript errors

### API Not Working

**Issue**: Frontend cannot connect to backend API.

**Solution**:
1. Verify `VITE_API_URL` is set in Vercel environment variables
2. Check that the backend is running and accessible
3. Ensure CORS is enabled on the backend
4. Test the backend URL directly (e.g., `https://your-backend.com/api/v1/health`)

### Build Failed

**Issue**: Vercel build fails with errors.

**Solution**:
1. Check Node.js version in Vercel settings (must be 18.x or higher)
2. Review build logs for specific error messages
3. Ensure all dependencies are in `package.json`
4. Test build locally: `npm run build`

### Environment Variables Not Loading

**Issue**: `VITE_API_URL` is undefined in production.

**Solution**:
1. Ensure variable name starts with `VITE_`
2. Redeploy after adding environment variables
3. Check that variables are set for the correct environment (Production/Preview/Development)

## Custom Domain (Optional)

To use a custom domain:

1. Go to **Project Settings → Domains**
2. Add your domain (e.g., `ccgt.example.com`)
3. Follow Vercel's DNS configuration instructions
4. SSL certificates are automatically provisioned

## Final Notes

- **Commit this guide**: Add `DEPLOYMENT_GUIDE.md` to your repository root
- **Update README**: Add your deployed Vercel link to `README.md`
- **Monitor deployments**: Check Vercel dashboard for build status and logs
- **Performance**: Vercel automatically optimizes assets and provides CDN caching

## Support

For issues specific to:
- **Vercel**: Check [Vercel Documentation](https://vercel.com/docs)
- **Vite**: See [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)
- **Project**: Open an issue on [GitHub](https://github.com/Skileated/CCGT)

---

**Deployed Example**: `https://ccgt.vercel.app`

**Last Updated**: November 2025

