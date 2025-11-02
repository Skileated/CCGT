@echo off
REM Start CCGT Backend Server (Windows)

echo Starting CCGT Backend Server...
echo.

cd /d "%~dp0..\backend"

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies if needed
echo Checking dependencies...
pip install -q -r requirements.txt

REM Start the server
echo.
echo Starting FastAPI server...
echo Backend will be available at http://127.0.0.1:8000
echo API docs available at http://127.0.0.1:8000/docs
echo.
python -m app.main

pause

