@echo off
REM Start CCGT Backend Server Standalone (Windows)
REM Use this if run_local.py doesn't work

echo Starting CCGT Backend Server...
echo.

cd /d "%~dp0..\backend"

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies if needed
echo Checking dependencies...
pip install -q -r requirements.txt

REM Start the server
echo.
echo ================================================
echo Starting FastAPI server...
echo Backend will be available at http://127.0.0.1:8000
echo API docs available at http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

python -m app.main

if errorlevel 1 (
    echo.
    echo ERROR: Backend failed to start
    echo Check the error messages above
    pause
)

