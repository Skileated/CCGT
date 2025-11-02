#!/usr/bin/env python3
"""
Alternative backend server runner.

Use this if python -m app.main doesn't work.
Run: python run_server.py
"""

import uvicorn
import sys
import os
from pathlib import Path

# Set unbuffered output
os.environ['PYTHONUNBUFFERED'] = '1'

# Ensure we're in the backend directory
backend_dir = Path(__file__).parent
os.chdir(backend_dir)

# Add to path
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

print("Loading application...")
sys.stdout.flush()

try:
    from app.main import app
    from app.core.config import settings
except Exception as e:
    print(f"\n{'='*60}")
    print("ERROR: Failed to import application")
    print(f"{'='*60}")
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
    print(f"\n{'='*60}")
    print("\nTroubleshooting:")
    print("1. Make sure virtual environment is activated")
    print("2. Run: pip install -r requirements.txt")
    print("3. Check for missing dependencies")
    sys.exit(1)

print(f"\n{'='*60}")
print(f"Starting CCGT API on http://{settings.HOST}:{settings.PORT}")
print(f"API docs available at http://{settings.HOST}:{settings.PORT}/docs")
print(f"{'='*60}\n")
sys.stdout.flush()

try:
    config = uvicorn.Config(
        app=app,
        host=settings.HOST,
        port=settings.PORT,
        log_level="info",
        reload=False,
        access_log=True
    )
    server = uvicorn.Server(config)
    server.run()
except KeyboardInterrupt:
    print("\nShutting down server...")
    sys.exit(0)
except Exception as e:
    print(f"\nERROR: Server failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

