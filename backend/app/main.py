import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import admin, agent, auth, buyers, impact, matches, messages, transactions, waste
from app.db.database import init_db
from app.services import agent_service
from waste2worth_ai import llm
from waste2worth_ai.impact_factors import FACTORS

BASE_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = BASE_DIR / "static"

init_db()

app = FastAPI(title="Waste2Worth Backend")

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.0.101:3000",
]
frontend_url = os.environ.get("FRONTEND_URL")
if frontend_url:
    ALLOWED_ORIGINS.append(frontend_url.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR.mkdir(parents=True, exist_ok=True)
(STATIC_DIR / "uploads").mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(waste.router, prefix="/waste", tags=["Waste"])
app.include_router(buyers.router, prefix="/buyers", tags=["Buyers"])
app.include_router(matches.router, prefix="/matches", tags=["Matches"])
app.include_router(agent.router, prefix="/agent", tags=["Agent"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(impact.router, prefix="/impact", tags=["Impact"])


@app.get("/")
def home():
    return {
        "message": "Waste2Worth backend is running",
        "docs": "/docs",
        "modules": ["auth", "waste", "buyers", "matches", "agent", "transactions", "messages", "admin", "impact"],
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "ai_enabled": llm.ai_enabled(),
        "openai_key_present": llm.has_api_key(),
        "smtp_enabled": agent_service.smtp_configured(),
        "impact_model_version": FACTORS["version"],
    }