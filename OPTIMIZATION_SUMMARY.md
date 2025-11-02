# CCGT Optimization Summary

## Changes Made

### 🗑️ Removed Docker Components

**Deleted Files:**
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `docker-compose.yml`
- `frontend/nginx.conf`
- `scripts/start_dev.sh` (replaced with Windows batch scripts)

**Updated:**
- `.github/workflows/ci.yml` - Removed Docker build steps, added frontend build test

### ⚙️ Memory Optimizations (6GB RAM Target)

#### Backend Optimizations

1. **Reduced Batch Size**
   - Changed from 32 to 8 sentences per batch
   - Location: `backend/app/core/config.py`

2. **Float16 Precision**
   - Embeddings converted to float16 (half precision)
   - Saves ~50% memory on embeddings
   - Location: `backend/app/models/embeddings.py`

3. **CPU-Only Inference**
   - Forced CPU device (no CUDA checks)
   - All tensors explicitly on CPU
   - Location: `backend/app/core/config.py`, `backend/app/pipeline/graph_builder.py`

4. **Memory-Efficient Model Loading**
   - Lazy loading (model loads on first request)
   - Gradient computation disabled
   - `torch.no_grad()` for all inference
   - Location: `backend/app/models/embeddings.py`, `backend/app/models/model.py`

5. **Single Worker Server**
   - FastAPI runs with 1 worker (not multiple)
   - Location: `backend/app/core/config.py`

6. **Embedding Caching**
   - File-based cache for embeddings
   - Reduces redundant computations
   - Location: `backend/app/models/embeddings.py`

#### Configuration Changes

```python
# backend/app/core/config.py
BATCH_SIZE: int = 8  # Reduced from 32
USE_FLOAT16: bool = True  # New setting
DEVICE: str = "cpu"  # Force CPU
WORKERS: int = 1  # Single worker
HOST: str = "127.0.0.1"  # Local only
```

### 🪟 Windows Optimization

1. **Windows Batch Scripts**
   - `scripts/start_backend.bat` - Start backend server
   - `scripts/start_frontend.bat` - Start frontend server
   - `scripts/download_models.bat` - Download models

2. **Python Launcher**
   - `run_local.py` - Cross-platform launcher (works on Windows)
   - Automatically handles venv creation
   - Starts both services

3. **Path Fixes**
   - All paths use Windows-style (`\`) where needed
   - Virtual environment activation: `venv\Scripts\activate`

### 📚 Documentation Updates

1. **README.md**
   - Removed all Docker references
   - Added Windows-specific instructions
   - Updated URLs to use `127.0.0.1:8000` and `127.0.0.1:5173`
   - Added PowerShell examples

2. **LOCAL_SETUP.md** (New)
   - Comprehensive Windows setup guide
   - Troubleshooting section
   - Performance tips

3. **QUICKSTART.md** (Updated)
   - Removed Docker commands
   - Added local execution examples

### 🌐 Frontend Updates

1. **Port Changes**
   - Changed from port 3000 to 5173 (Vite default)
   - Updated API URL to `127.0.0.1:8000`

2. **Configuration**
   - `frontend/vite.config.ts` - Updated host and proxy
   - `frontend/src/api.ts` - Updated default API URL

## Memory Usage Breakdown

| Component | Estimated Memory |
|-----------|------------------|
| Python Runtime | ~100 MB |
| FastAPI Server | ~50 MB |
| Sentence-BERT Model | ~400-600 MB (on first load) |
| Embeddings (float16, 8 sentences) | ~10-20 MB |
| Graph Data | ~5-10 MB |
| PyTorch/PyG | ~200-300 MB |
| **Total (steady state)** | **~1-2 GB** |
| **Peak (model loading)** | **~3-4 GB** |

**With 6GB available RAM, the system should run comfortably.**

## Performance Characteristics

- **First Request**: ~3-5 seconds (model loading)
- **Subsequent Requests**: ~1-2 seconds (model cached)
- **Memory Footprint**: ~1-2 GB steady state
- **CPU Usage**: Moderate (single-threaded inference)

## Verification Checklist

- [x] Docker files removed
- [x] Memory optimizations applied
- [x] Windows batch scripts created
- [x] Documentation updated
- [x] CI/CD updated (no Docker)
- [x] Local URLs updated (127.0.0.1)
- [x] Frontend port updated (5173)
- [x] CPU-only inference enforced
- [x] Float16 embeddings enabled
- [x] Batch size reduced (8)

## Running Locally

### Quick Start:
```cmd
python run_local.py
```

### Manual Start:
```cmd
REM Terminal 1
cd backend
venv\Scripts\activate
python -m app.main

REM Terminal 2
cd frontend
npm run dev
```

### Access:
- Frontend: http://127.0.0.1:5173
- Backend API: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs

## Notes

- Model downloads on first use (~400MB)
- First request is slower due to model loading
- Subsequent requests are faster due to caching
- Memory usage is optimized but can be further reduced by:
  - Reducing batch size to 4
  - Disabling float16 (if stability issues)
  - Using smaller model variant

