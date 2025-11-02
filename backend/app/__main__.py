"""Entry point for running the application directly."""

if __name__ == "__main__":
    import uvicorn
    from app.main import app
    from app.core.config import settings
    
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)

