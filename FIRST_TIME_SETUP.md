# First-Time Setup Guide - CCGT

This is a comprehensive step-by-step guide for setting up and running CCGT for the first time on Windows.

## 📋 Prerequisites Checklist

Before you begin, make sure you have:

- [ ] **Windows 10/11** installed
- [ ] **Python 3.11 or higher** installed
- [ ] **Node.js 18 or higher** installed
- [ ] **~2 GB free disk space** (for dependencies and models)
- [ ] **~6 GB available RAM** (optimized for this)
- [ ] **Internet connection** (for downloading models)

### Step 1: Verify Prerequisites

#### Check Python Installation

Open Command Prompt (cmd) or PowerShell and run:

```cmd
python --version
```

**Expected output:** `Python 3.11.x` or higher

**If Python is not installed:**
1. Download from [python.org](https://www.python.org/downloads/)
2. During installation, **check the box "Add Python to PATH"**
3. Restart your terminal after installation

#### Check Node.js Installation

```cmd
node --version
npm --version
```

**Expected output:** `v18.x.x` or higher for both

**If Node.js is not installed:**
1. Download from [nodejs.org](https://nodejs.org/)
2. Install the LTS (Long Term Support) version
3. Restart your terminal after installation

#### Check Available Space

Make sure you have at least 2 GB free space on your drive.

---

## 🚀 Step 2: Get the Project

If you haven't already, extract or clone the CCGT project to a folder. For example:

```
C:\Users\YourName\Desktop\SWE_CCGT
```

**Navigate to the project folder:**

```cmd
cd C:\Users\YourName\Desktop\SWE_CCGT
```

*(Replace with your actual path)*

---

## 🐍 Step 3: Set Up Python Virtual Environment

### 3.1 Navigate to Backend Directory

```cmd
cd backend
```

### 3.2 Create Virtual Environment

```cmd
python -m venv venv
```

**What this does:** Creates an isolated Python environment for the project.

**Expected output:** No errors. A `venv` folder will be created.

### 3.3 Activate Virtual Environment

```cmd
venv\Scripts\activate
```

**Expected output:** Your prompt should change to show `(venv)` at the beginning:
```
(venv) C:\Users\YourName\Desktop\SWE_CCGT\backend>
```

**If you see an error about execution policy:**
Run this in PowerShell (as Administrator):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📦 Step 4: Install Python Dependencies

### 4.1 Navigate Back to Root (or install from root)

**Option A: Install from project root (recommended)**

```cmd
cd ..
pip install -r requirements.txt
```

**Option B: Install from backend directory**

```cmd
pip install -r requirements.txt
```

**What this does:** Installs all required Python packages.

**Expected duration:** 5-15 minutes depending on your internet speed.

**Expected output:** You'll see packages being downloaded and installed. At the end, you should see:
```
Successfully installed [list of packages]
```

**Common issues:**

- **"pip is not recognized"**: Make sure Python is in your PATH
- **"Requirement already satisfied"**: That's fine, means it's already installed
- **Slow download**: This is normal, packages are large

### 4.2 Verify Installation

```cmd
python -c "import fastapi, torch, sentence_transformers; print('✓ All core dependencies installed!')"
```

**Expected output:** `✓ All core dependencies installed!`

---

## 📥 Step 5: Download NLP Models

### 5.1 Download spaCy Model

```cmd
python -m spacy download en_core_web_sm
```

**What this does:** Downloads the English language model for sentence segmentation.

**Expected duration:** 1-3 minutes

**Expected output:**
```
✓ Download and installation successful
You can now load the package via spacy.load("en_core_web_sm")
```

### 5.2 Download Sentence-BERT Model

**This is the largest download (~400 MB). It will happen automatically on first use, but you can download it now:**

**Option A: Manual download (recommended)**

```cmd
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-mpnet-base-v2', cache_folder='./models')"
```

**Option B: Use the batch script**

```cmd
cd ..
scripts\download_models.bat
```

**What this does:** Downloads the Sentence-BERT model for generating embeddings.

**Expected duration:** 5-10 minutes (depends on internet speed)

**Expected output:** Model download progress, then completion message.

**Note:** The model will be cached in `backend/models/` folder. First download is the slowest.

---

## 🎨 Step 6: Set Up Frontend

### 6.1 Navigate to Frontend Directory

Open a **NEW** terminal window (keep the backend terminal open) and run:

```cmd
cd C:\Users\YourName\Desktop\SWE_CCGT\frontend
```

*(Replace with your actual path)*

### 6.2 Install Node.js Dependencies

```cmd
npm install
```

**What this does:** Installs React, TypeScript, and all frontend dependencies.

**Expected duration:** 2-5 minutes

**Expected output:** 
```
added [number] packages, and audited [number] packages in [time]
```

**Note:** You may see some warnings - that's normal. Look for "added" or "up to date" messages.

---

## 🏃 Step 7: Run the Application

You have two options:

### Option A: Automatic Launch (Easiest)

From the project root directory, run:

```cmd
cd C:\Users\YourName\Desktop\SWE_CCGT
python run_local.py
```

**What this does:** 
- Starts both backend and frontend automatically
- Opens your browser to the frontend
- Shows status messages

**Expected output:**
```
============================================================
  CCGT Local Development Launcher
============================================================

📦 Checking backend dependencies...
🚀 Starting backend server...
🚀 Starting frontend server...

============================================================
  Services started successfully!
============================================================

📍 Backend API: http://127.0.0.1:8000
   API Docs:    http://127.0.0.1:8000/docs
📍 Frontend:    http://127.0.0.1:5173

Press Ctrl+C to stop all services
```

**To stop:** Press `Ctrl+C` in the terminal.

### Option B: Manual Launch (Two Terminals)

#### Terminal 1 - Backend

```cmd
cd C:\Users\YourName\Desktop\SWE_CCGT\backend
venv\Scripts\activate
python -m app.main
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Keep this terminal open!**

#### Terminal 2 - Frontend

Open a **new** terminal window:

```cmd
cd C:\Users\YourName\Desktop\SWE_CCGT\frontend
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  ready in [time] ms

  ➜  Local:   http://127.0.0.1:5173/
  ➜  Network: use --host to expose
```

**Keep this terminal open too!**

---

## ✅ Step 8: Verify Everything Works

### 8.1 Check Backend API

Open your web browser and go to:

```
http://127.0.0.1:8000/docs
```

**Expected:** You should see the Swagger API documentation page with interactive API explorer.

### 8.2 Check Frontend

Open your web browser and go to:

```
http://127.0.0.1:5173
```

**Expected:** You should see the CCGT homepage with a text input area.

### 8.3 Test API with Sample Text

#### Using PowerShell:

```powershell
$body = @{
    text = "The field of natural language processing has advanced significantly. Machine learning models can now understand text. Coherence evaluation helps measure text quality."
    options = @{ visualize = $true }
} | ConvertTo-Json

Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/evaluate -Method Post -Body $body -ContentType "application/json"
```

#### Using curl (if installed):

```cmd
curl -X POST http://127.0.0.1:8000/api/v1/evaluate -H "Content-Type: application/json" -d "{\"text\": \"This is a test paragraph. It has multiple sentences. They should be coherent.\", \"options\": {\"visualize\": true}}"
```

**Expected output:** A JSON response with `coherence_score`, `coherence_percent`, `disruption_report`, and `graph` data.

### 8.4 Test Frontend

1. Go to http://127.0.0.1:5173
2. Paste some text in the textarea (e.g., the sample text above)
3. Click "Evaluate Coherence"
4. **Expected:** You should see:
   - Coherence score displayed
   - Graph visualization (if text has multiple sentences)
   - Disruption report (if any issues found)

---

## 🎉 Success Checklist

If everything worked, you should have:

- [x] Backend running on http://127.0.0.1:8000
- [x] Frontend running on http://127.0.0.1:5173
- [x] API docs accessible at http://127.0.0.1:8000/docs
- [x] Can evaluate text through API
- [x] Can evaluate text through frontend
- [x] Graph visualization working (for multi-sentence text)

---

## 🛠️ Troubleshooting

### Problem: "Python is not recognized"

**Solution:**
1. Reinstall Python and check "Add Python to PATH"
2. Or manually add Python to PATH in System Environment Variables
3. Restart terminal after adding to PATH

### Problem: "pip is not recognized"

**Solution:**
```cmd
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Problem: "ModuleNotFoundError" when running

**Solution:**
1. Make sure virtual environment is activated (you should see `(venv)` in prompt)
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Make sure you're in the correct directory

### Problem: Backend won't start

**Solution:**
1. Check if port 8000 is in use:
   ```cmd
   netstat -ano | findstr :8000
   ```
2. If port is in use, change port in `backend/app/core/config.py`:
   ```python
   PORT: int = 8001  # Change from 8000
   ```
3. Make sure models are downloaded (see Step 5)

### Problem: Frontend won't start

**Solution:**
1. Delete `node_modules` and reinstall:
   ```cmd
   cd frontend
   rmdir /s /q node_modules
   npm install
   ```
2. Check if port 5173 is in use (Vite will try next port automatically)

### Problem: "Model not found" error

**Solution:**
1. Make sure you downloaded the Sentence-BERT model (Step 5.2)
2. Check that `backend/models/` folder exists
3. Re-download the model if needed

### Problem: Slow first request

**Solution:** This is normal! The model loads on the first request (takes 3-5 seconds). Subsequent requests will be faster.

### Problem: Out of memory errors

**Solution:**
1. Close other applications to free RAM
2. Reduce batch size in `backend/app/core/config.py`:
   ```python
   BATCH_SIZE: int = 4  # Reduce from 8
   ```

### Problem: Can't access frontend from browser

**Solution:**
1. Check that frontend is running (look at terminal output)
2. Try accessing http://127.0.0.1:5173 (not localhost)
3. Check firewall settings

---

## 📚 Next Steps

Once everything is working:

1. **Explore the API**: Visit http://127.0.0.1:8000/docs for interactive API explorer
2. **Try the CLI**: 
   ```cmd
   python cli/ccgt_cli.py evaluate --text "Your text here"
   ```
3. **Run the notebook**: Open `notebooks/demo.ipynb` in Jupyter
4. **Read the docs**: Check `README.md` for more information

---

## 💡 Quick Reference

### Start Everything (Automatic)
```cmd
python run_local.py
```

### Start Backend Only
```cmd
cd backend
venv\Scripts\activate
python -m app.main
```

### Start Frontend Only
```cmd
cd frontend
npm run dev
```

### Stop Services
- Press `Ctrl+C` in the terminal(s) running the services

---

## 📞 Getting Help

If you encounter issues not covered here:

1. Check `LOCAL_SETUP.md` for detailed setup instructions
2. Check `INSTALL.md` for installation troubleshooting
3. Check `README.md` for general information
4. Review error messages carefully - they often contain helpful information

---

**Congratulations! You've successfully set up CCGT! 🎉**

Now you can evaluate text coherence using graph-based transformer models.

