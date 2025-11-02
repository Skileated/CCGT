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
import os
import threading
import queue

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
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5, shell=True)
        if result.returncode != 0:
            issues.append("Node.js not found in PATH")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        issues.append("Node.js not found in PATH - please install from nodejs.org")
    
    # Check npm
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, timeout=5, shell=True)
        if result.returncode != 0:
            issues.append("npm not found in PATH")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        issues.append("npm not found in PATH - npm comes with Node.js")
    
    return issues

def start_backend():
    """Start the FastAPI backend server."""
    backend_dir = Path(__file__).parent / "backend"
    
    # Verify backend directory exists
    if not backend_dir.exists():
        raise FileNotFoundError(f"Backend directory not found: {backend_dir}")
    
    # Check if venv exists
    venv_python = backend_dir / "venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        print_status("⚠ Virtual environment not found. Creating...", YELLOW)
        result = subprocess.run(
            [sys.executable, "-m", "venv", "venv"],
            cwd=backend_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to create virtual environment: {result.stderr}")
        venv_python = backend_dir / "venv" / "Scripts" / "python.exe"
    
    # Activate venv and run
    python_exe = str(venv_python)
    
    # Install dependencies if needed
    print_status("📦 Checking backend dependencies...", BLUE)
    result = subprocess.run(
        [python_exe, "-m", "pip", "install", "-q", "-r", "requirements.txt"],
        cwd=backend_dir,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print_status("⚠ Some dependencies may not be installed correctly", YELLOW)
    
    print_status("🚀 Starting backend server...", GREEN)
    # Start backend with proper output handling
    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
    
    proc = subprocess.Popen(
        [python_exe, "-m", "app.main"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env
    )
    
    # Wait and check if it crashed immediately
    time.sleep(3)
    if proc.poll() is not None:
        # Process exited - try to read error
        error_output = ""
        try:
            output_queue = queue.Queue()
            
            def read_output():
                try:
                    for line in iter(proc.stdout.readline, ''):
                        if line:
                            output_queue.put(line)
                except:
                    pass
            
            reader_thread = threading.Thread(target=read_output, daemon=True)
            reader_thread.start()
            reader_thread.join(timeout=2)
            
            while not output_queue.empty():
                error_output += output_queue.get()
        except:
            try:
                remaining, _ = proc.communicate(timeout=1)
                if remaining:
                    error_output += remaining
            except:
                pass
        
        if error_output:
            print_status("Backend error output:", RED)
            print(error_output[:1000])
        else:
            print_status(f"Backend exited with code: {proc.returncode}", RED)
        
        print_status("\n⚠ Backend failed to start!", RED)
        print_status("Start backend manually to see full errors:", YELLOW)
        print_status("  cd backend", BLUE)
        print_status("  venv\\Scripts\\activate", BLUE)
        print_status("  python -m app.main", BLUE)
        raise RuntimeError("Backend process exited immediately. Start it manually to debug.")
    
    print_status("✓ Backend process started", GREEN)
    return proc

def start_frontend():
    """Start the frontend development server."""
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Verify frontend directory exists
    if not frontend_dir.exists():
        raise FileNotFoundError(f"Frontend directory not found: {frontend_dir}")
    
    # Check if npm is available
    try:
        subprocess.run(["npm", "--version"], capture_output=True, text=True, timeout=5, shell=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        raise FileNotFoundError(
            "npm not found in PATH. Please:\n"
            "1. Install Node.js from https://nodejs.org/\n"
            "2. Restart your terminal after installation\n"
            "3. Verify with: npm --version"
        )
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print_status("📦 Installing frontend dependencies...", BLUE)
        result = subprocess.run(
            ["npm", "install"],
            cwd=frontend_dir,
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"npm install failed: {result.stderr}")
    
    print_status("🚀 Starting frontend server...", GREEN)
    try:
        return subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True  # Use shell=True on Windows
        )
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Failed to start frontend: {e}\n"
            "Make sure npm is in your PATH. Try:\n"
            "1. Restart your terminal\n"
            "2. Check with: npm --version\n"
            "3. If not found, reinstall Node.js"
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
        print_status("Please install missing dependencies before continuing.", RED)
        print_status("Node.js: https://nodejs.org/", BLUE)
        print_status("Python: https://www.python.org/downloads/", BLUE)
        print()
        response = input("Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            sys.exit(1)
        print()
    
    processes = []
    
    try:
        # Start backend
        try:
            backend_proc = start_backend()
            processes.append(("backend", backend_proc))
            time.sleep(2)
        except Exception as e:
            print_status(f"❌ Failed to start backend: {e}", RED)
            raise
        
        # Start frontend
        try:
            frontend_proc = start_frontend()
            processes.append(("frontend", frontend_proc))
            time.sleep(3)
        except FileNotFoundError as e:
            print_status(f"❌ Failed to start frontend: {e}", RED)
            print_status("⚠ Backend is still running. You can access it at http://127.0.0.1:8000", YELLOW)
            raise
        except Exception as e:
            print_status(f"❌ Failed to start frontend: {e}", RED)
            raise
        
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
        print_status("💡 IMPORTANT: If backend exits, start it manually:", BLUE)
        print_status("   cd backend && venv\\Scripts\\activate && python -m app.main", BLUE)
        print()
        
        # Open browser
        time.sleep(2)
        try:
            webbrowser.open("http://127.0.0.1:5173")
        except:
            pass
        
        # Monitor processes
        backend_exit_warned = False
        
        while True:
            # Check backend
            backend_proc = next((p for n, p in processes if n == "backend"), None)
            if backend_proc and backend_proc.poll() is not None:
                if not backend_exit_warned:
                    backend_exit_warned = True
                    exit_code = backend_proc.returncode
                    print_status("\n" + "="*60, RED)
                    print_status("  ❌ CRITICAL: Backend exited!", RED)
                    print_status("="*60, RED)
                    print_status(f"Exit code: {exit_code}", RED)
                    print_status("\n⚠ Frontend cannot connect without backend!", YELLOW)
                    print_status("\nTo fix, start backend in a SEPARATE terminal:", YELLOW)
                    print_status("  1. Open new PowerShell", BLUE)
                    print_status("  2. Run:", BLUE)
                    print_status("     cd C:\\Users\\Nishant V.S\\Desktop\\SWE_CCGT\\backend", BLUE)
                    print_status("     venv\\Scripts\\activate", BLUE)
                    print_status("     python -m app.main", BLUE)
                    print_status("  3. Keep that terminal open!", BLUE)
                    print_status("\nOr use: scripts\\test_backend.bat", BLUE)
                    print_status("\nFrontend is still running. Backend must be restarted separately.", YELLOW)
                    print()
            
            # Check frontend
            frontend_proc = next((p for n, p in processes if n == "frontend"), None)
            if frontend_proc and frontend_proc.poll() is not None:
                exit_code = frontend_proc.returncode
                if exit_code != 0:
                    print_status(f"\n⚠ Frontend exited with error (code: {exit_code})", RED)
                    break
            
            # Check if all stopped
            if all(p.poll() is not None for _, p in processes):
                break
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print()
        print_status("🛑 Stopping services...", YELLOW)
        for name, proc in processes:
            if proc:
                try:
                    proc.terminate()
                    proc.wait(timeout=5)
                    print_status(f"✓ {name} stopped", GREEN)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    print_status(f"⚠ {name} force killed", YELLOW)
                except:
                    pass
        print_status("All services stopped", GREEN)
    except Exception as e:
        print()
        print_status(f"❌ Error: {e}", RED)
        print_status("🛑 Stopping services...", YELLOW)
        for name, proc in processes:
            if proc:
                try:
                    proc.terminate()
                    proc.wait(timeout=2)
                except:
                    try:
                        proc.kill()
                    except:
                        pass
        print()
        print_status("See QUICK_FIX.md or BACKEND_CONNECTION_FIX.md for help", BLUE)
        sys.exit(1)

if __name__ == "__main__":
    main()
