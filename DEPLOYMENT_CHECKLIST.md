# CCGT Deployment Checklist

Quick reference for deploying frontend (Vercel) and backend (Render).

## ✅ Completed Configuration

### Backend (Render-ready)
- ✅ `render.yaml` created at project root
- ✅ `backend/runtime.txt` specifies Python 3.11
- ✅ `backend/app/core/config.py` reads PORT from environment
- ✅ `backend/app/main.py` CORS configured (reads from CORS_ORIGINS env var)
- ✅ `backend/app/api/v1/contact.py` uses reliable file paths
- ✅ `backend/requirements.txt` contains all dependencies

### Frontend (Vercel-ready)
- ✅ `frontend/src/api.ts` uses `VITE_API_URL` environment variable
- ✅ Already deployed on Vercel
- ✅ Build configuration complete

## 🚀 Deployment Steps

### Step 1: Push Changes to GitHub

```bash
# Commit all changes
git add .
git commit -m "Add Render deployment configuration and CORS updates"
git push origin main
```

### Step 2: Deploy Backend to Render

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **New +** → **Blueprint** (or **Web Service**)
3. **Connect GitHub** repository
4. **If using Blueprint**: Render auto-detects `render.yaml`
5. **If manual setup**:
   - **Name**: `ccgt-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. **Set Environment Variables**:
   ```
   HOST=0.0.0.0
   DEVICE=cpu
   LOG_LEVEL=INFO
   OPTIMIZED_MODE=true
   CACHE_EMBEDDINGS=true
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   ```
7. **Deploy** and wait for completion (5-10 minutes first time)
8. **Note your backend URL**: `https://ccgt-backend.onrender.com`

### Step 3: Configure Frontend (Vercel)

1. **Go to Vercel Dashboard** → Your project → **Settings** → **Environment Variables**
2. **Add**:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://ccgt-backend.onrender.com` (your Render URL)
   - **Environments**: Production, Preview, Development
3. **Save** and **Redeploy** frontend (or push a commit to trigger auto-deploy)

### Step 4: Verify Deployment

#### Test Backend
```bash
# Health check
curl https://ccgt-backend.onrender.com/api/v1/health

# Root endpoint
curl https://ccgt-backend.onrender.com/
```

#### Test Frontend
1. Open your Vercel URL: `https://your-app.vercel.app`
2. Open browser DevTools → Network tab
3. Navigate to **Try Demo** page
4. Enter text and click **Evaluate Coherence**
5. Verify:
   - ✅ API call goes to Render backend
   - ✅ No CORS errors in console
   - ✅ Results display correctly

## 📝 Quick Reference

### Backend URLs
- **Local**: `http://127.0.0.1:8000`
- **Render**: `https://ccgt-backend.onrender.com` (example)

### Frontend URLs
- **Local**: `http://localhost:5173`
- **Vercel**: `https://your-app.vercel.app`

### Environment Variables

**Render (Backend)**:
```
HOST=0.0.0.0
DEVICE=cpu
LOG_LEVEL=INFO
OPTIMIZED_MODE=true
CACHE_EMBEDDINGS=true
CORS_ORIGINS=https://your-vercel-app.vercel.app
```

**Vercel (Frontend)**:
```
VITE_API_URL=https://ccgt-backend.onrender.com
```

## 🔧 Troubleshooting

### Backend Issues
- **Build fails**: Check Render logs for dependency errors
- **Service won't start**: Verify PORT env var is set (Render provides automatically)
- **CORS errors**: Update CORS_ORIGINS with exact Vercel URL

### Frontend Issues
- **API not working**: Verify VITE_API_URL is set in Vercel
- **Build fails**: Run `npm run build` locally to check for errors
- **Connection refused**: Check that backend is running on Render

## 📚 Documentation

- **Full Render Guide**: See `RENDER_DEPLOYMENT.md`
- **Vercel Guide**: See `DEPLOYMENT_GUIDE.md`
- **Backend API Docs**: `https://your-backend.onrender.com/docs` (after deployment)

---

**Status**: ✅ Ready for deployment

