"""
routers/resume_view.py
Resume View API — serves anonymized resume data for the view-resume page.

Prefix : /api/resumes
Tags   : Resume View
"""

from __future__ import annotations
from fastapi import APIRouter, HTTPException

import db
from anonymizer import anonymize_resume, anonymize_batch

router = APIRouter(prefix="/api/resumes", tags=["Resume View"])


# ── GET /api/resumes ──────────────────────────────────────────────────────────
@router.get(
    "",
    summary="All anonymized resumes",
    description="Returns every candidate record with PII stripped — used by the resume-view candidate switcher.",
)
def get_all_resumes():
    all_c = db.get_all_candidates()
    return {"success": True, "candidates": anonymize_batch(all_c)}


# ── GET /api/resumes/{candidate_id} ──────────────────────────────────────────
@router.get(
    "/{candidate_id}",
    summary="Single anonymized resume",
)
def get_resume(candidate_id: str):
    raw = db.get_candidate_by_id(candidate_id)
    if raw is None:
        raise HTTPException(status_code=404, detail=f"Candidate {candidate_id} not found")
    return {"success": True, "candidate": anonymize_resume(raw)}
