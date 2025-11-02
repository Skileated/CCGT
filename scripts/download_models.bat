@echo off
REM Download Sentence-BERT model weights (Windows)

echo Downloading Sentence-BERT model: sentence-transformers/all-mpnet-base-v2
echo.

cd /d "%~dp0..\backend"

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install sentence-transformers if not already installed
pip install -q sentence-transformers

REM Download model
echo Loading and caching model...
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-mpnet-base-v2', cache_folder='./models')"

echo.
echo Model download complete!
echo Model cached in: backend\models

pause

