from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import admin, agent, auth, buyers, matches, messages, transactions, waste
from app.db.database import init_db

BASE_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = BASE_DIR / "static"

init_db()

app = FastAPI(title="Waste2Worth Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.0.101:3000",
    ],
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


@app.get("/")
def home():
    return {
        "message": "Waste2Worth backend is running",
        "docs": "/docs",
        "modules": ["auth", "waste", "buyers", "matches", "agent", "transactions", "messages", "admin"],
    }