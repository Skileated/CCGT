# CCGT Backend Deployment Guide (Render)

This guide walks you through deploying the CCGT FastAPI backend to Render and connecting it to your Vercel frontend.

## Prerequisites

- GitHub repository with your code
- Render account ([sign up here](https://render.com))
- Vercel frontend already deployed (optional, but recommended)

## Step 1: Prepare Backend for Render

The backend is already configured with:
- ✅ `render.yaml` - Render deployment configuration
- ✅ `runtime.txt` - Python version specification
- ✅ `requirements.txt` - All dependencies
- ✅ Environment-aware configuration (reads PORT from Render)
- ✅ CORS middleware configured for frontend access

## Step 2: Deploy Backend to Render

### Option A: Using render.yaml (Recommended)

1. **Push code to GitHub**
   ```bash
   git add backend/render.yaml backend/runtime.txt backend/app/core/config.py backend/app/main.py
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. **Create Render Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Review settings and click **"Apply"**

3. **Manual Configuration** (if not using Blueprint)
   - Go to **"New +"** → **"Web Service"**
   - Connect your GitHub repository
   - Configure:
     - **Name**: `ccgt-backend`
     - **Root Directory**: `backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - **Plan**: Starter (or higher for better performance)

4. **Set Environment Variables** (in Render Dashboard → Environment)
   ```
   HOST=0.0.0.0
   PORT=$PORT (Render provides this automatically)
   DEVICE=cpu
   LOG_LEVEL=INFO
   OPTIMIZED_MODE=true
   CACHE_EMBEDDINGS=true
   CORS_ORIGINS=https://your-vercel-app.vercel.app,https://your-vercel-app-git-main.vercel.app
   ```

   **Important**: Replace `your-vercel-app` with your actual Vercel deployment URL.

5. **Deploy**
   - Render will automatically build and deploy
   - First deployment takes 5-10 minutes (model download)
   - Note your backend URL: `https://ccgt-backend.onrender.com` (example)

### Option B: Using Render CLI

```bash
# Install Render CLI
npm install -g render-cli

# Login
render login

# Deploy from backend directory
cd backend
render deploy
```

## Step 3: Configure Frontend to Connect to Backend

1. **Get your Render backend URL**
   - After deployment, find your service URL in Render dashboard
   - Example: `https://ccgt-backend.onrender.com`

2. **Update Vercel Environment Variables**
   - Go to your Vercel project → **Settings** → **Environment Variables**
   - Add new variable:
     - **Name**: `VITE_API_URL`
     - **Value**: `https://ccgt-backend.onrender.com` (your Render URL)
     - **Environment**: Production, Preview, Development

3. **Redeploy Frontend**
   - Vercel will automatically redeploy when you push changes
   - Or manually trigger: **Deployments** → **Redeploy**

## Step 4: Verify Deployment

### Backend Health Check

Test the backend directly:

```bash
# Health endpoint
curl https://ccgt-backend.onrender.com/api/v1/health

# Root endpoint
curl https://ccgt-backend.onrender.com/
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Frontend Connection Test

1. Open your Vercel frontend: `https://your-app.vercel.app`
2. Open browser DevTools → Network tab
3. Try evaluating text in the Demo page
4. Check that API calls go to your Render backend URL
5. Verify no CORS errors in console

### Test API Endpoints

```bash
# Test evaluation endpoint
curl -X POST https://ccgt-backend.onrender.com/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test paragraph. It contains multiple sentences.", "options": {"visualize": true}}'
```

## Step 5: Production Optimizations

### Render Service Settings

1. **Auto-Deploy**: Enable auto-deploy from main branch
2. **Health Check**: Set to `/api/v1/health`
3. **Plan**: Consider upgrading if you need:
   - More RAM (models need ~2-4GB)
   - Faster cold starts
   - Better performance

### Environment Variables (Production)

Recommended settings in Render:

```
HOST=0.0.0.0
DEVICE=cpu
LOG_LEVEL=INFO
OPTIMIZED_MODE=true
CACHE_EMBEDDINGS=true
BATCH_SIZE=8
CORS_ORIGINS=https://your-vercel-app.vercel.app,https://your-vercel-app-git-main.vercel.app
```

**Security Note**: Replace wildcard `CORS_ORIGINS=*` with your specific Vercel URLs in production.

## Troubleshooting

### Backend Won't Start

**Issue**: Build succeeds but service fails to start.

**Solution**:
1. Check Render logs for error messages
2. Verify start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Ensure `PORT` environment variable is set (Render provides this automatically)
4. Check that all dependencies installed correctly

### CORS Errors

**Issue**: Frontend can't connect to backend (CORS errors in browser).

**Solution**:
1. Verify `CORS_ORIGINS` includes your Vercel URL
2. Check backend logs for CORS-related errors
3. Test with `CORS_ORIGINS=*` temporarily (then restrict to specific domains)
4. Ensure frontend uses `https://` (not `http://`) for Render backend

### Slow First Request

**Issue**: First API request takes 30+ seconds.

**Solution**: This is normal! The model loads on first request. Subsequent requests are faster (2-5 seconds).

### Out of Memory Errors

**Issue**: Render service crashes with memory errors.

**Solution**:
1. Upgrade to a higher Render plan (more RAM)
2. Reduce `BATCH_SIZE` in environment variables
3. Set `USE_FLOAT16=true` (already enabled)
4. Consider using a smaller model variant

### Model Download Issues

**Issue**: Build fails during model download.

**Solution**:
1. Models download automatically on first use (not during build)
2. First request may take longer while models download
3. Check Render logs for download progress
4. Ensure internet connectivity in Render environment

## Monitoring

### Render Dashboard

- **Logs**: View real-time logs in Render dashboard
- **Metrics**: Monitor CPU, memory, and response times
- **Events**: Track deployments and service restarts

### Health Monitoring

Set up uptime monitoring:
- Ping `/api/v1/health` endpoint every 5 minutes
- Use services like UptimeRobot or Pingdom
- Alert on failures

## Cost Estimation

Render Starter Plan:
- **Free tier**: 750 hours/month (suitable for testing)
- **Starter ($7/month)**: Always-on service
- **Standard ($25/month)**: Better performance, more resources

**Recommendation**: Start with Starter plan, upgrade if needed.

## Next Steps

1. ✅ Backend deployed to Render
2. ✅ Frontend configured with `VITE_API_URL`
3. ✅ CORS configured correctly
4. ✅ Health checks passing
5. ✅ Test end-to-end flow

## Support

- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Project Issues**: Open issue on GitHub

---

**Last Updated**: November 2025

