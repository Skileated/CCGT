# Fix: Backend Connection Refused Error

## Problem
Frontend shows `ERR_CONNECTION_REFUSED` when trying to connect to `http://127.0.0.1:8000/api/v1/evaluate`

This means the backend server is not running or not accessible.

## Quick Fix Steps

### Step 1: Start Backend Manually (To See Errors)

Open a **new terminal/PowerShell window** and run:

```cmd
cd C:\Users\Nishant V.S\Desktop\SWE_CCGT\backend
venv\Scripts\activate
python -m app.main
```

**Watch for errors!** Common issues:
- Import errors
- Port already in use
- Missing dependencies
- Model loading errors

### Step 2: Verify Backend is Running

Once you see this output, backend is running:
```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Keep this terminal open!** If you close it, backend stops.

### Step 3: Test Backend in Browser

Open http://127.0.0.1:8000/docs in your browser. You should see the API documentation.

If this works, the backend is running correctly.

### Step 4: Test Frontend Connection

Go back to your frontend at http://127.0.0.1:5173 and try evaluating text again.

## Alternative: Use Standalone Backend Script

If `run_local.py` doesn't work, use:

```cmd
scripts\start_backend_standalone.bat
```

This will:
- Create venv if needed
- Install dependencies
- Start backend with visible output
- Show any errors clearly

## Common Issues & Solutions

### Issue 1: Backend Crashes Immediately

**Symptoms:** Backend starts then exits right away

**Solution:**
1. Check the error message in terminal
2. Common causes:
   - Missing dependencies: `pip install -r requirements.txt`
   - Import errors: Check Python path
   - Port conflict: Change port or kill process using port 8000

### Issue 2: Port 8000 Already in Use

**Check what's using port 8000:**
```cmd
netstat -ano | findstr :8000
```

**Kill the process:**
```cmd
taskkill /PID <process_id> /F
```

**Or change port** in `backend/app/core/config.py`:
```python
PORT: int = 8001  # Change from 8000
```

Then update frontend API URL in `frontend/src/api.ts`:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001';
```

### Issue 3: Import Errors

**Error:** `ModuleNotFoundError` or `ImportError`

**Solution:**
1. Make sure virtual environment is activated (`venv\Scripts\activate`)
2. Install dependencies: `pip install -r requirements.txt`
3. Make sure you're in the `backend` directory when running

### Issue 4: Virtual Environment Not Found

**Solution:**
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Verification Checklist

- [ ] Backend terminal shows "Uvicorn running on http://127.0.0.1:8000"
- [ ] Can access http://127.0.0.1:8000/docs in browser
- [ ] Health endpoint works: http://127.0.0.1:8000/api/v1/health
- [ ] Frontend is running on http://127.0.0.1:5173
- [ ] No firewall blocking localhost connections

## Recommended: Run Backend and Frontend Separately

**Terminal 1 - Backend:**
```cmd
cd backend
venv\Scripts\activate
python -m app.main
```

**Terminal 2 - Frontend:**
```cmd
cd frontend
npm run dev
```

This way you can see errors from both services clearly.

