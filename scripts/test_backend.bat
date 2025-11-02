@echo off
REM Test backend startup and show any errors

echo Testing backend startup...
echo.

cd /d "%~dp0..\backend"

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Run: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Test import
echo Testing imports...
python -c "from app.main import app; print('✓ App imports successfully')"

if errorlevel 1 (
    echo.
    echo ERROR: Failed to import app
    echo Check the error above
    echo.
    echo Trying alternative import test...
    python -c "import app.main" 2>&1
    pause
    exit /b 1
)

echo.
echo Testing alternative startup method...
echo.

REM Try run_server.py first (has better error handling)
if exist "run_server.py" (
    echo Using run_server.py...
    python run_server.py
) else (
    echo Using python -m app.main...
    python -m app.main
)

if errorlevel 1 (
    echo.
    echo ERROR: Backend failed to start
    echo Check the error above
    pause
    exit /b 1
)

pause

