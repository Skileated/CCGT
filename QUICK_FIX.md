# Quick Fix: Backend Keeps Exiting

## The Problem
Backend starts but immediately exits with code 0 (clean exit). Frontend cannot connect.

## Immediate Solution

**Start backend manually in a separate terminal:**

1. **Open PowerShell (as Administrator if needed)**

2. **Navigate and start backend:**
   ```powershell
   cd C:\Users\Nishant V.S\Desktop\SWE_CCGT\backend
   venv\Scripts\activate
   python -m app.main
   ```

3. **Watch for errors** - You should see:
   ```
   ============================================================
   Starting CCGT API on http://127.0.0.1:8000
   API docs available at http://127.0.0.1:8000/docs
   ============================================================
   
   INFO:     Started server process
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```

4. **Keep this terminal open!** The backend must stay running.

5. **In another terminal, start frontend:**
   ```powershell
   cd C:\Users\Nishant V.S\Desktop\SWE_CCGT\frontend
   npm run dev
   ```

## Alternative: Use Test Script

```cmd
scripts\test_backend.bat
```

This will show any import errors or startup issues clearly.

## Why This Happens

The backend process in `run_local.py` is exiting because:
- The process completes its initialization and exits
- uvicorn might not be blocking properly
- There could be an import or configuration error

Running it manually shows the actual error messages.

## After Backend is Running

1. Open http://127.0.0.1:8000/docs - Should show API documentation
2. Open http://127.0.0.1:5173 or http://127.0.0.1:5174 - Frontend should connect
3. Try evaluating text - Should work now!

## Common Errors When Starting Manually

### ImportError or ModuleNotFoundError
```cmd
pip install -r requirements.txt
```

### Port already in use
```cmd
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### ConfigDict error
This should be fixed, but if you see it:
- Check `backend/app/schemas.py` has `from pydantic import BaseModel, Field, ConfigDict`

## Permanent Fix

Once you identify why the backend exits (from manual start), we can fix `run_local.py` accordingly.

