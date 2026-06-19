"""
main.py
ElastiCrew FastAPI application — entry point.

Endpoints:
  /api/resume-queue/**  — queue CRUD + status management
  /api/resumes/**       — anonymized resume view data
  /api/statuses         — valid status values and pipeline stages
  /*                    — static frontend files (parent directory)

Run:
  uvicorn main:app --reload --port 3000
"""

from __future__ import annotations
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routers import resume_queue, resume_view
import db

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="ElastiCrew API",
    description=(
        "Resume anonymization, queue management, and hiring pipeline APIs "
        "for the ElastiCrew platform."
    ),
    version="2.0.0",
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(resume_queue.router)
app.include_router(resume_view.router)

# ── GET /api/statuses ─────────────────────────────────────────────────────────
@app.get("/api/statuses", tags=["Meta"], summary="Valid statuses and pipeline stages")
def get_statuses():
    return {
        "success": True,
        "resume_statuses": db.ResumeStatus.all_values(),
        "pipeline_stages": db.PIPELINE_STAGES,
    }

# ── Static frontend ───────────────────────────────────────────────────────────
# Serves all HTML / CSS / JS from the parent directory (project root).
_FRONTEND_DIR = Path(__file__).parent.parent  # …/Elasticrew-main

# Mount static assets (css, js, images) — must come AFTER API routes
app.mount("/static", StaticFiles(directory=str(_FRONTEND_DIR)), name="static")

@app.get("/{full_path:path}", include_in_schema=False)
def serve_frontend(full_path: str):
    """
    Catch-all: try to serve the requested file from the frontend directory;
    fall back to index.html for any unmatched path (SPA support).
    """
    target = _FRONTEND_DIR / full_path
    if target.is_file():
        return FileResponse(str(target))
    index = _FRONTEND_DIR / "index.html"
    if index.is_file():
        return FileResponse(str(index))
    return {"detail": "Not found"}
