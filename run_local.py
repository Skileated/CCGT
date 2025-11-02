#!/usr/bin/env python3
"""
Local development launcher for CCGT.

Starts both backend and frontend services locally on Windows.
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import signal
import os

# Color codes for Windows terminal
try:
    import colorama
    colorama.init()
    GREEN = colorama.Fore.GREEN
    YELLOW = colorama.Fore.YELLOW
    BLUE = colorama.Fore.BLUE
    RED = colorama.Fore.RED
    RESET = colorama.Style.RESET_ALL
except ImportError:
    GREEN = YELLOW = BLUE = RED = RESET = ""

def print_status(message, color=GREEN):
    """Print colored status message."""
    print(f"{color}{message}{RESET}")

def check_dependencies():
    """Check if required dependencies are installed."""
    issues = []
    
    # Check Python
    if sys.version_info < (3, 11):
        issues.append(f"Python 3.11+ required (found {sys.version_info.major}.{sys.version_info.minor})")
    
    # Check Node.js (basic check)
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            issues.append("Node.js not found in PATH")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        issues.append("Node.js not found in PATH")
    
    return issues

def start_backend():
    """Start the FastAPI backend server."""
    backend_dir = Path(__file__).parent / "backend"
    
    # Check if venv exists
    venv_python = backend_dir / "venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        print_status("⚠ Virtual environment not found. Creating...", YELLOW)
        subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=backend_dir)
        venv_python = backend_dir / "venv" / "Scripts" / "python.exe"
    
    # Activate venv and run
    python_exe = str(venv_python)
    
    # Install dependencies if needed
    print_status("📦 Checking backend dependencies...", BLUE)
    subprocess.run([python_exe, "-m", "pip", "install", "-q", "-r", "requirements.txt"], 
                  cwd=backend_dir)
    
    print_status("🚀 Starting backend server...", GREEN)
    return subprocess.Popen(
        [python_exe, "-m", "app.main"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

def start_frontend():
    """Start the frontend development server."""
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print_status("📦 Installing frontend dependencies...", BLUE)
        subprocess.run(["npm", "install"], cwd=frontend_dir)
    
    print_status("🚀 Starting frontend server...", GREEN)
    return subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

def main():
    """Main launcher function."""
    print_status("=" * 60, BLUE)
    print_status("  CCGT Local Development Launcher", BLUE)
    print_status("=" * 60, BLUE)
    print()
    
    # Check dependencies
    issues = check_dependencies()
    if issues:
        print_status("⚠ Dependency issues found:", YELLOW)
        for issue in issues:
            print_status(f"  - {issue}", YELLOW)
        print()
        response = input("Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            sys.exit(1)
    
    processes = []
    
    try:
        # Start backend
        backend_proc = start_backend()
        processes.append(("backend", backend_proc))
        time.sleep(2)  # Wait for backend to start
        
        # Start frontend
        frontend_proc = start_frontend()
        processes.append(("frontend", frontend_proc))
        time.sleep(3)  # Wait for frontend to start
        
        print()
        print_status("=" * 60, GREEN)
        print_status("  Services started successfully!", GREEN)
        print_status("=" * 60, GREEN)
        print()
        print_status("📍 Backend API: http://127.0.0.1:8000", BLUE)
        print_status("   API Docs:    http://127.0.0.1:8000/docs", BLUE)
        print_status("📍 Frontend:    http://127.0.0.1:5173", BLUE)
        print()
        print_status("Press Ctrl+C to stop all services", YELLOW)
        print()
        
        # Open browser after delay
        time.sleep(2)
        try:
            webbrowser.open("http://127.0.0.1:5173")
        except:
            pass
        
        # Wait for processes
        while True:
            for name, proc in processes:
                if proc.poll() is not None:
                    print_status(f"⚠ {name} process exited unexpectedly", RED)
                    print_status(f"   Exit code: {proc.returncode}", RED)
                    if proc.stderr:
                        print(proc.stderr.read())
                    raise KeyboardInterrupt
            time.sleep(1)
            
    except KeyboardInterrupt:
        print()
        print_status("🛑 Stopping services...", YELLOW)
        for name, proc in processes:
            proc.terminate()
            try:
                proc.wait(timeout=5)
                print_status(f"✓ {name} stopped", GREEN)
            except subprocess.TimeoutExpired:
                proc.kill()
                print_status(f"⚠ {name} force killed", YELLOW)
        print_status("All services stopped", GREEN)

if __name__ == "__main__":
    main()

