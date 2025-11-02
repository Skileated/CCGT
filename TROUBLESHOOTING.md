# Troubleshooting Guide

Common issues and solutions when running CCGT.

## npm/Node.js Not Found

### Error:
```
FileNotFoundError: [WinError 2] The system cannot find the file specified
```

### Solution:

1. **Check if Node.js is installed:**
   ```cmd
   node --version
   npm --version
   ```

2. **If not installed:**
   - Download Node.js from https://nodejs.org/
   - Install the LTS (Long Term Support) version
   - **Important:** Restart your terminal/command prompt after installation

3. **If installed but not found:**
   - Close and reopen your terminal
   - Check if Node.js is in PATH:
     ```cmd
     where node
     where npm
     ```
   - If not in PATH, manually add it:
     1. Find Node.js installation (usually `C:\Program Files\nodejs\`)
     2. Add to System Environment Variables > PATH
     3. Restart terminal

4. **Verify installation:**
   ```cmd
   node --version
   npm --version
   ```
   Both should return version numbers.

5. **Try running frontend manually:**
   ```cmd
   cd frontend
   npm --version
   npm install
   npm run dev
   ```

## Python Not Found

### Error:
```
'python' is not recognized as an internal or external command
```

### Solution:

1. **Check if Python is installed:**
   ```cmd
   python --version
   ```

2. **If not installed:**
   - Download from https://www.python.org/downloads/
   - During installation, **check "Add Python to PATH"**
   - Restart terminal after installation

3. **If installed but not found:**
   - Use full path or `py` launcher:
     ```cmd
     py --version
     ```
   - Or add Python to PATH manually

## Virtual Environment Issues

### Error:
```
ModuleNotFoundError: No module named 'app'
```

### Solution:

1. **Make sure virtual environment is activated:**
   ```cmd
   cd backend
   venv\Scripts\activate
   ```
   You should see `(venv)` in your prompt.

2. **Reinstall dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Create fresh virtual environment:**
   ```cmd
   cd backend
   rmdir /s /q venv
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Port Already in Use

### Error:
```
Address already in use
Port 8000 is already in use
```

### Solution:

1. **Find process using port:**
   ```cmd
   netstat -ano | findstr :8000
   ```

2. **Kill the process:**
   ```cmd
   taskkill /PID <process_id> /F
   ```

3. **Or change port in config:**
   Edit `backend/app/core/config.py`:
   ```python
   PORT: int = 8001  # Change from 8000
   ```

## Model Loading Errors

### Error:
```
OSError: Can't load tokenizer
Model not found
```

### Solution:

1. **Download models manually:**
   ```cmd
   cd backend
   venv\Scripts\activate
   python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-mpnet-base-v2', cache_folder='./models')"
   ```

2. **Download spaCy model:**
   ```cmd
   python -m spacy download en_core_web_sm
   ```

3. **Check model directory:**
   - Ensure `backend/models/` exists
   - Check disk space (models need ~400MB)

## Frontend Build Errors

### Error:
```
npm ERR! code ELIFECYCLE
npm ERR! errno 1
```

### Solution:

1. **Clear npm cache:**
   ```cmd
   npm cache clean --force
   ```

2. **Delete node_modules and reinstall:**
   ```cmd
   cd frontend
   rmdir /s /q node_modules
   del package-lock.json
   npm install
   ```

3. **Check Node.js version:**
   - Requires Node.js 18+
   - Update if needed from nodejs.org

## Memory Errors

### Error:
```
OutOfMemoryError
Killed
```

### Solution:

1. **Close other applications** to free RAM

2. **Reduce batch size** in `backend/app/core/config.py`:
   ```python
   BATCH_SIZE: int = 4  # Reduce from 8
   ```

3. **Disable float16** (uses more memory but may be more stable):
   ```python
   USE_FLOAT16: bool = False
   ```

## Import Errors

### Error:
```
ImportError: cannot import name 'X' from 'Y'
```

### Solution:

1. **Make sure you're in the correct directory:**
   ```cmd
   cd backend
   ```

2. **Activate virtual environment:**
   ```cmd
   venv\Scripts\activate
   ```

3. **Reinstall dependencies:**
   ```cmd
   pip install --upgrade -r requirements.txt
   ```

4. **Check Python path:**
   ```cmd
   python -c "import sys; print(sys.path)"
   ```

## Frontend Not Connecting to Backend

### Symptoms:
- Frontend loads but shows errors
- API calls fail
- Network errors in browser console

### Solution:

1. **Verify backend is running:**
   - Check http://127.0.0.1:8000/docs in browser
   - Should show API documentation

2. **Check API URL in frontend:**
   - Edit `frontend/src/api.ts`
   - Ensure `API_BASE_URL` is `http://127.0.0.1:8000`

3. **Check CORS settings:**
   - Backend should allow all origins (for local dev)
   - Check `backend/app/main.py` CORS configuration

4. **Check firewall:**
   - Windows Firewall may be blocking connections
   - Allow Python and Node.js through firewall

## run_local.py Script Issues

### Error:
```
FileNotFoundError: The system cannot find the file specified
```

### Solution:

1. **Make sure you're in project root:**
   ```cmd
   cd C:\Users\YourName\Desktop\SWE_CCGT
   ```

2. **Check file exists:**
   ```cmd
   dir run_local.py
   ```

3. **Run with full Python path:**
   ```cmd
   C:\Python311\python.exe run_local.py
   ```

4. **Try manual start instead:**
   - Use separate terminals for backend and frontend
   - See FIRST_TIME_SETUP.md for manual instructions

## Still Having Issues?

1. **Check logs:**
   - Backend: Look at terminal output
   - Frontend: Check browser console (F12)

2. **Verify versions:**
   ```cmd
   python --version  # Should be 3.11+
   node --version    # Should be 18+
   npm --version
   ```

3. **Check file structure:**
   ```
   SWE_CCGT/
   ├── backend/
   ├── frontend/
   ├── run_local.py
   └── requirements.txt
   ```

4. **Re-read setup guide:**
   - See FIRST_TIME_SETUP.md for complete setup
   - See LOCAL_SETUP.md for detailed instructions

5. **Common fixes:**
   - Restart terminal/computer
   - Reinstall dependencies
   - Create fresh virtual environment
   - Check internet connection (for model downloads)

