import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="AEGIS-AI",
    description="Adaptive Geopolitical Event Intelligence System",
    version="1.0.0",
)

# ALLOWED_ORIGINS: comma-separated list of allowed frontend origins.
# Production example (set this on Render):
#   ALLOWED_ORIGINS=https://aegis-ai.vercel.app
# Leave unset for local development — defaults to localhost.
_raw_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
