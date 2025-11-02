# Debug Backend Startup

## Problem
Running `python -m app.main` produces no output and returns to prompt immediately.

## Quick Tests

### Test 1: Check if imports work
```powershell
cd backend
venv\Scripts\activate
python -c "from app.main import app; print('Import successful')"
```

### Test 2: Check for syntax errors
```powershell
python -m py_compile app/main.py
python -m py_compile app/__main__.py
```

### Test 3: Run alternative script
```powershell
python run_server.py
```

### Test 4: Check uvicorn directly
```powershell
python -c "import uvicorn; print(uvicorn.__version__)"
```

## Common Issues

### Issue: No output at all
**Possible causes:**
- Import error happens before print statements
- Python path issue
- Module not found

**Solution:**
1. Run test 1 above - if it fails, there's an import error
2. Check error with: `python -c "import app.main" 2>&1`
3. Try: `python run_server.py` instead

### Issue: ConfigDict error
**Solution:**
- Already fixed, but verify: `grep ConfigDict backend/app/schemas.py`

### Issue: Port already in use
**Solution:**
```powershell
netstat -ano | findstr :8000
taskkill /PID <pid> /F
```

## Alternative: Use uvicorn command directly

```powershell
cd backend
venv\Scripts\activate
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

This bypasses `__main__.py` entirely and might reveal the actual issue.

