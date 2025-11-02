# Installation Guide

This guide covers different ways to install CCGT dependencies.

## Quick Install (Recommended)

From the project root:

```bash
pip install -r requirements.txt
```

This installs all core dependencies needed to run the backend and CLI.

## Installation Options

### 1. Full Installation (Default)

```bash
pip install -r requirements.txt
```

**Includes:**
- Core backend dependencies (FastAPI, PyTorch, etc.)
- ML libraries (sentence-transformers, PyTorch Geometric)
- CLI tools (Typer)
- Testing tools (pytest)
- Utilities (colorama for terminal colors)

### 2. Minimal Installation (Production)

```bash
pip install -r requirements-minimal.txt
```

**Includes:**
- Only production dependencies
- No testing tools
- Smaller footprint

### 3. Development Installation

```bash
pip install -r requirements-dev.txt
```

**Includes:**
- Everything from `requirements.txt`
- Development tools (ruff, black, isort)
- Type checking (mypy)
- Notebook dependencies (jupyter, matplotlib, networkx)

### 4. Backend-Only Installation

```bash
cd backend
pip install -r requirements.txt
```

Installs only backend-specific dependencies (same as root `requirements.txt`).

## Virtual Environment Setup

**Recommended:** Always use a virtual environment:

```cmd
REM Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Post-Installation Steps

After installing dependencies, you need to download models:

### 1. Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 2. Download Sentence-BERT Model

The model will be downloaded automatically on first use, or manually:

```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-mpnet-base-v2')"
```

Or use the batch script:
```cmd
scripts\download_models.bat
```

## Verification

Check if installation was successful:

```python
python -c "import fastapi, torch, sentence_transformers; print('All dependencies installed!')"
```

## Troubleshooting

### PyTorch Installation Issues

If PyTorch installation fails:

```bash
# For CPU-only (recommended for this project)
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Memory Issues During Installation

If installation consumes too much memory:

1. Install in smaller batches
2. Use `--no-cache-dir` flag:
   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

### Version Conflicts

If you encounter version conflicts:

1. Create a fresh virtual environment
2. Upgrade pip: `python -m pip install --upgrade pip`
3. Install dependencies: `pip install -r requirements.txt`

## File Locations

- **Root `requirements.txt`**: Main requirements file (all dependencies)
- **`requirements-minimal.txt`**: Production-only dependencies
- **`requirements-dev.txt`**: Development dependencies
- **`backend/requirements.txt`**: Backend-specific (duplicate of root)

All requirements files are equivalent - use whichever is most convenient for your setup.

