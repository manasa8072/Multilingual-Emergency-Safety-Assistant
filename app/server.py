"""
FastAPI Server for Multilingual Emergency & Safety Assistant.
Exposes REST endpoints:
- POST /api/analyze: Analyzes raw emergency text input
- GET /api/metrics: Returns offline model evaluation accuracy & confusion matrices
- GET /api/examples: Returns preset sample messages (English, Tamil, Tanglish)
- GET /: Serves compiled React frontend if present
"""

import os
import sys
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.assistant import EmergencyAssistant

app = FastAPI(
    title="Multilingual Emergency & Safety Assistant API",
    description="AI-powered emergency understanding for English, Tamil, and Tanglish",
    version="1.0.0"
)

# Enable CORS for local Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize assistant once (loads models)
try:
    assistant = EmergencyAssistant()
    print("[Server] Successfully loaded models into EmergencyAssistant.")
except Exception as e:
    print(f"[Server Warning] Could not load models on startup: {e}")
    assistant = None


class EmergencyRequest(BaseModel):
    text: str = Field(..., description="The user's emergency message")


PRESET_EXAMPLES = [
    {
        "id": "ex1",
        "label": "English Medical",
        "language": "English",
        "category": "Medical",
        "text": "I need an ambulance immediately, 1 person unconscious near City Hospital"
    },
    {
        "id": "ex2",
        "label": "Tamil Fire",
        "language": "Tamil",
        "category": "Fire",
        "text": "எங்கள் வீட்டில் தீப்பிடித்துவிட்டது"
    },
    {
        "id": "ex3",
        "label": "Tanglish Accident",
        "language": "Tanglish",
        "category": "Accident",
        "text": "Road la accident aayiduchu, someone badly injured"
    },
    {
        "id": "ex4",
        "label": "Tanglish Location & Injury",
        "language": "Tanglish",
        "category": "Accident",
        "text": "Road la accident aayiduchu near Thoothukudi bus stand, 2 people injured"
    },
    {
        "id": "ex5",
        "label": "Tanglish Safety",
        "language": "Tanglish",
        "category": "Police / Crime",
        "text": "Yaaro enna follow panranga"
    },
    {
        "id": "ex6",
        "label": "Tamil Natural Disaster",
        "language": "Tamil",
        "category": "Natural Disaster",
        "text": "எங்கள் பகுதியில் வெள்ளம் ஏற்பட்டுள்ளது, 5 பேர் சிக்கியுள்ளனர்"
    }
]


@app.post("/api/analyze")
def analyze_emergency(req: EmergencyRequest):
    global assistant
    if assistant is None:
        try:
            assistant = EmergencyAssistant()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Models not loaded: {str(e)}")
            
    res = assistant.analyze(req.text)
    if not res.get("success"):
        return JSONResponse(status_code=400, content=res)
    return res


@app.get("/api/metrics")
def get_metrics():
    metrics_path = PROJECT_ROOT / "model" / "model_metrics.json"
    if metrics_path.exists():
        with open(metrics_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"message": "Metrics not found. Please run training/evaluate_models.py"}


@app.get("/api/examples")
def get_examples():
    return PRESET_EXAMPLES


# Mount compiled frontend dist if available
FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")

    @app.get("/")
    def serve_index():
        index_file = FRONTEND_DIST / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"message": "Frontend index.html not found"}

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        target = FRONTEND_DIST / full_path
        if target.exists() and target.is_file():
            return FileResponse(target)
        index_file = FRONTEND_DIST / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"message": "Frontend build not found."}


if __name__ == "__main__":
    import uvicorn
    print("\nStarting Multilingual Emergency & Safety Assistant server...")
    print("Open http://127.0.0.1:8000 in your browser\n")
    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=False)
