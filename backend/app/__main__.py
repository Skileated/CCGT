"""Entry point for running the application directly."""

if __name__ == "__main__":
    import uvicorn
    import sys
    import os
    
    # Set unbuffered output for immediate logging
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    # Add parent directory to path to allow importing app
    from pathlib import Path
    backend_dir = Path(__file__).parent.parent
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))
    
    # Import here so errors are caught and displayed
    try:
        from app.main import app
        from app.core.config import settings
    except Exception as e:
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"ERROR: Failed to import app", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)
        print(f"\nError details: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        print(f"\n{'='*60}", file=sys.stderr)
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"Starting CCGT API on http://{settings.HOST}:{settings.PORT}")
    print(f"API docs available at http://{settings.HOST}:{settings.PORT}/docs")
    print(f"{'='*60}\n")
    sys.stdout.flush()  # Ensure output is flushed
    
    # Use uvicorn Server with proper blocking
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
        print("Server starting...")
        sys.stdout.flush()
        server.run()  # This blocks until server stops
    except KeyboardInterrupt:
        print("\nShutting down backend server...")
        sys.exit(0)
    except Exception as e:
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"ERROR: Backend failed to start: {e}", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

