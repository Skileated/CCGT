@echo off
REM Start CCGT Frontend Server (Windows)

echo Starting CCGT Frontend Server...
echo.

cd /d "%~dp0..\frontend"

REM Install dependencies if needed
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)

REM Start development server
echo.
echo Starting Vite development server...
echo Frontend will be available at http://127.0.0.1:5173
echo.
call npm run dev

pause

