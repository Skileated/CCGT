# Local Setup Guide (Windows)

This guide walks you through setting up and running CCGT on a Windows machine without Docker.

## System Requirements

- **OS**: Windows 10/11
- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **RAM**: ~6 GB available (project optimized for limited memory)
- **Disk**: ~2 GB free space (for models and dependencies)

## Step 1: Install Prerequisites

### Python 3.11+

1. Download from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation:
   ```cmd
   python --version
   ```

### Node.js 18+

1. Download from [nodejs.org](https://nodejs.org/)
2. Verify installation:
   ```cmd
   node --version
   npm --version
   ```

## Step 2: Clone/Download Project

Extract or clone the project to a directory, e.g.:
```
C:\Users\YourName\Desktop\SWE_CCGT
```

## Step 3: Backend Setup

```cmd
cd backend

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
venv\Scripts\activate

REM Install dependencies
REM Option 1: Install from root (includes all dependencies)
cd ..
pip install -r requirements.txt

REM Option 2: Install from backend directory (backend-specific)
REM pip install -r requirements.txt

REM Download spaCy model (first time only)
python -m spacy download en_core_web_sm

REM Download Sentence-BERT model (first time only, ~400MB)
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-mpnet-base-v2')"
```

**Note**: The Sentence-BERT model download may take several minutes on first run.

## Step 4: Frontend Setup

Open a new terminal window:

```cmd
cd frontend

REM Install dependencies (first time only)
npm install
```

## Step 5: Run the Application

### Option A: Use the Launcher Script (Easiest)

From the project root:

```cmd
python run_local.py
```

This will start both backend and frontend automatically.

### Option B: Manual Start

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

### Option C: Use Batch Scripts

**Backend:**
```cmd
scripts\start_backend.bat
```

**Frontend:**
```cmd
scripts\start_frontend.bat
```

## Step 6: Access the Application

Once running:

- **Frontend Dashboard**: http://127.0.0.1:5173
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

## Testing the API

### Using PowerShell:

```powershell
# Health check
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/health

# Evaluate text
$body = @{
    text = "The field of natural language processing has advanced significantly. Machine learning models can now understand text. Coherence evaluation is important."
    options = @{ visualize = $true }
} | ConvertTo-Json

Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/evaluate -Method Post -Body $body -ContentType "application/json"
```

### Using curl (if installed):

```cmd
curl http://127.0.0.1:8000/api/v1/health

curl -X POST http://127.0.0.1:8000/api/v1/evaluate ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"Your text here\", \"options\": {\"visualize\": true}}"
```

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError`
```cmd
# Ensure virtual environment is activated
venv\Scripts\activate
pip install -r requirements.txt
```

**Problem**: Model download fails
```cmd
# Try downloading manually
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-mpnet-base-v2', cache_folder='./models')"
```

**Problem**: Port 8000 already in use
- Change port in `backend/app/core/config.py`: `PORT: int = 8001`
- Or stop the process using port 8000

### Frontend Issues

**Problem**: `npm install` fails
```cmd
# Clear cache and retry
npm cache clean --force
npm install
```

**Problem**: Port 5173 already in use
- Vite will automatically try the next available port
- Or change port in `frontend/vite.config.ts`

### Memory Issues

If you encounter out-of-memory errors:

1. **Reduce batch size** in `backend/app/core/config.py`:
   ```python
   BATCH_SIZE: int = 4  # Reduce from 8
   ```

2. **Disable float16** (uses more memory but may be more stable):
   ```python
   USE_FLOAT16: bool = False
   ```

3. **Close other applications** to free up RAM

## Performance Tips

- **First request is slower**: Model loads on first use (lazy loading)
- **Subsequent requests are faster**: Embeddings are cached
- **Memory usage**: ~2-4 GB typical, ~6 GB peak during model load

## Next Steps

- See `README.md` for full documentation
- Check `examples/` for sample data
- Explore `notebooks/demo.ipynb` for pipeline walkthrough

