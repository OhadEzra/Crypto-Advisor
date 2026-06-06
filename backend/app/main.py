import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth, dashboard, users, admin

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Moveo AI Crypto Advisor", version="1.0.0")

frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

allowed_origins = [
    frontend_origin,
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        frontend_origin,
        "http://localhost:5173",
    ],
    allow_origin_regex=r"https://.*vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-crypto-advisor", "version": "1.0.0"}
