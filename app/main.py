from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, waste, buyers, matches
from app.db.database import Base, engine
from app.models import user, waste as waste_model, buyer, match

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Waste2Worth Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(waste.router, prefix="/waste", tags=["Waste"])
app.include_router(buyers.router, prefix="/buyers", tags=["Buyers"])
app.include_router(matches.router, prefix="/matches", tags=["Matches"])

@app.get("/")
def home():
    return {"message": "Waste2Worth backend is running"}
