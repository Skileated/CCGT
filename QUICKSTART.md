# Quick Start Guide

## First Time Setup

**👉 New users: See [FIRST_TIME_SETUP.md](FIRST_TIME_SETUP.md) for complete step-by-step guide**

## Fastest Way to Run (After Setup)

1. **Automatic Launch (Recommended):**
   ```cmd
   python run_local.py
   ```

2. **Access the services:**
   - Frontend: http://127.0.0.1:5173
   - Backend API: http://127.0.0.1:8000
   - API Docs: http://127.0.0.1:8000/docs

3. **Test the API:**
   ```powershell
   Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/health
   ```
   
   Or with curl:
   ```cmd
   curl http://127.0.0.1:8000/api/v1/health
   ```

## Example API Call

**PowerShell:**
```powershell
$body = @{
    text = "This is a sample paragraph. It contains multiple sentences. Each sentence should flow coherently to the next."
    options = @{ visualize = $true }
} | ConvertTo-Json

Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/evaluate -Method Post -Body $body -ContentType "application/json"
```

**curl:**
```cmd
curl -X POST http://127.0.0.1:8000/api/v1/evaluate -H "Content-Type: application/json" -d "{\"text\": \"This is a sample paragraph. It contains multiple sentences. Each sentence should flow coherently.\", \"options\": {\"visualize\": true}}"
```

## Example CLI Usage

```bash
# Evaluate a text file
python cli/ccgt_cli.py evaluate --text "Your paragraph text here" --visualize

# Evaluate from file
python cli/ccgt_cli.py evaluate --file examples/paragraphs.json
```

## Troubleshooting

- **Models not loading**: Run `scripts\download_models.bat` or see Step 5 in FIRST_TIME_SETUP.md
- **Port conflicts**: Change ports in `backend/app/core/config.py` (PORT) or `frontend/vite.config.ts` (server.port)
- **Frontend not connecting**: Check that backend is running and API is accessible at http://127.0.0.1:8000
- **Python not found**: Make sure Python is in PATH and virtual environment is activated
- **ModuleNotFoundError**: Reinstall dependencies: `pip install -r requirements.txt`

**For detailed troubleshooting, see [FIRST_TIME_SETUP.md](FIRST_TIME_SETUP.md)**

