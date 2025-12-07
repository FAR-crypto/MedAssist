# Multi-Agent Emergency Healthcare Triage (Demo)

This repository contains a demo multi-agent emergency triage system with a static frontend and a FastAPI backend.

Quick start (Windows PowerShell):

```powershell
Set-Location -Path 'C:\Users\A1\hackathon PW'
python -m venv .venv
# Activate environment
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Start backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# In a second shell, serve the frontend
python -m http.server 8080
# Open the UI in a browser
start http://localhost:8080/index.html
# Run the automated triage test
python scripts/test_triage.py
```

Notes:
- This is a demo; the triage outputs are illustrative only and not medical advice.
- For development, use the included `scripts/test_triage.py` to validate the API behaviour.

If you want, I can create/update `requirements.txt` to include the needed packages (FastAPI, uvicorn, pydantic, reportlab).