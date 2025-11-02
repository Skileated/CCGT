# CCGT: Contextual Coherence Graph Transformer

A production-ready system for evaluating textual coherence using graph-based transformer models. This project analyzes paragraph-level coherence by constructing semantic graphs from sentences and applying graph neural networks to compute coherence scores.

## Overview

CCGT evaluates textual coherence by:

1. **Preprocessing**: Sentence segmentation and discourse marker detection
2. **Embedding**: Generating semantic embeddings using Sentence-BERT
3. **Graph Construction**: Building semantic + discourse graphs with entropy-based features
4. **Graph Transformer**: Applying graph neural networks to compute coherence scores
5. **Explainability**: Identifying weak links and disruption points

## Architecture

- **Backend**: FastAPI (Python 3.11+) with PyTorch + PyTorch Geometric
- **Frontend**: React + TypeScript + Tailwind CSS + D3.js
- **ML Models**: Sentence-BERT (all-mpnet-base-v2) + Custom Graph Transformer
- **Storage**: File-based model storage and embedding cache

## Quick Start

### Prerequisites

- Python 3.11+ (for backend)
- Node.js 18+ (for frontend)
- Windows 10/11 (optimized for local Windows execution)
- ~6 GB available RAM recommended

### 🚀 First Time Setup

**New to CCGT? Start here:**

👉 **[See FIRST_TIME_SETUP.md for detailed step-by-step instructions](FIRST_TIME_SETUP.md)**

This guide walks you through:

- Installing prerequisites
- Setting up virtual environment
- Downloading models
- Running backend and frontend
- Testing the application

### 💻 Local Setup (Windows)

#### Option 1: Quick Start Script (Recommended)

```bash
# Run both backend and frontend
python run_local.py
```

This will:

- Check dependencies
- Create virtual environments if needed
- Start backend at http://127.0.0.1:8000
- Start frontend at http://127.0.0.1:5173
- Open browser automatically

#### Option 2: Manual Setup

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# Or install minimal (production only): pip install -r requirements-minimal.txt
# Or install with dev tools: pip install -r requirements-dev.txt

# Download spaCy model (first time only)
python -m spacy download en_core_web_sm

# Download Sentence-BERT models (first time only)
# This downloads ~400MB model weights
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-mpnet-base-v2')"

# Run backend server
python -m app.main
# Or: uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be available at: **http://127.0.0.1:8000**

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

Frontend will be available at: **http://127.0.0.1:5173**

### Windows Batch Scripts

You can also use the provided batch scripts:

```cmd
# Start backend only
scripts\start_backend.bat

# Start frontend only
scripts\start_frontend.bat
```

### Using the CLI

```bash
# Install CLI dependencies
pip install -r backend/requirements.txt

# Evaluate a text file
python cli/ccgt_cli.py evaluate --file mydoc.txt

# Save graph visualization
python cli/ccgt_cli.py evaluate --file mydoc.txt --save-graph graph.json
```

### Using the API

```bash
# Health check
curl http://127.0.0.1:8000/api/v1/health

# Evaluate text
curl -X POST http://127.0.0.1:8000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"This is a sample paragraph. It contains multiple sentences. Each sentence should flow coherently.\", \"options\": {\"visualize\": true}}"
```

Or use PowerShell:

```powershell
# Health check
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/health

# Evaluate text
$body = @{
    text = "This is a sample paragraph. It contains multiple sentences. Each sentence should flow coherently."
    options = @{ visualize = $true }
} | ConvertTo-Json

Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/evaluate -Method Post -Body $body -ContentType "application/json"
```

### API Response Format

```json
{
  "coherence_score": 0.82,
  "coherence_percent": 82,
  "disruption_report": [
    {
      "from_idx": 2,
      "to_idx": 3,
      "reason": "low_similarity",
      "score": 0.12
    }
  ],
  "graph": {
    "nodes": [
      {
        "id": 0,
        "text_snippet": "...",
        "entropy": 0.45,
        "importance_score": 0.8
      }
    ],
    "edges": [
      {
        "source": 0,
        "target": 1,
        "weight": 0.75,
        "reason": "semantic_similarity"
      }
    ]
  }
}
```

## Example Usage

See `notebooks/demo.ipynb` for a step-by-step walkthrough of the pipeline.

Sample input/output examples are in `examples/paragraphs.json` and `examples/sample_output.json`.

## Performance & Memory Optimization

- **Inference Latency**: ≤ 2s for 500 words on moderate CPU
- **Memory Usage**: Optimized for ~6GB available RAM
  - Batch size reduced to 8 sentences
  - Float16 precision for embeddings
  - CPU-only inference (no CUDA)
  - Lazy model loading
  - Embedding caching
- **Optimizations Applied**:
  - Single worker FastAPI server
  - `torch.no_grad()` for all inference
  - Gradient computation disabled
  - CPU tensor operations only

## API Documentation

Once the backend is running, visit:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Testing

```bash
cd backend
pytest tests/
```

## Project Structure

```
ccgt/
├── backend/          # FastAPI application
├── frontend/         # React dashboard
├── cli/              # Command-line interface
├── notebooks/        # Jupyter notebooks
├── examples/         # Sample data
├── scripts/           # Utility scripts
└── .github/          # CI/CD workflows
```

## Security

- JWT-based API authentication (optional, disabled by default for local dev)
- API keys configured via environment variables
- Input validation and sanitization
- See `backend/app/core/auth.py` for authentication details

**Note**: For local development, authentication is optional. Enable it in production by setting `SECRET_KEY` environment variable.

## Limitations & Future Improvements

- Current model optimized for English text
- Discourse marker detection uses fixed list (could be ML-based)
- Graph layout for visualization is force-directed (could use learned layouts)
- Batch processing could benefit from GPU acceleration
- Consider fine-tuning Sentence-BERT on coherence-specific datasets

## License

MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## Changelog

See CHANGELOG.md for version history and features.
