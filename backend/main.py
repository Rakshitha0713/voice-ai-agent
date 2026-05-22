import os
import sys
sys.path.insert(0, os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
))

from fastapi import FastAPI, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="2Care.ai Voice Agent", version="1.0.0")

# Templates
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "frontend", "templates")
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )


@app.get("/health")
def health():
    return {"status": "running", "service": "2Care.ai"}


@app.websocket("/ws/voice")
async def voice_websocket(websocket: WebSocket):
    from backend.api.websocket import voice_ws_endpoint
    await voice_ws_endpoint(websocket)


@app.on_event("startup")
async def startup():
    print("[SERVER] 2Care.ai Voice Agent started!")
    print("[SERVER] Open http://localhost:8000 in browser")