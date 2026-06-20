"""
routers/resume_view.py
Resume View API — serves anonymized resume data for the view-resume page.

Prefix : /api/resumes
Tags   : Resume View
"""

from __future__ import annotations
from fastapi import APIRouter, HTTPException

from sqlalchemy.orm import Session
from fastapi import Depends

from database import get_db
from models import Candidate
from anonymizer import anonymize_resume, anonymize_batch

router = APIRouter(prefix="/api/resumes", tags=["Resume View"])


# ── GET /api/resumes ──────────────────────────────────────────────────────────
@router.get(
    "",
    summary="All anonymized resumes",
    description="Returns every candidate record with PII stripped — used by the resume-view candidate switcher.",
)
def get_all_resumes(
    db: Session = Depends(get_db)
):
    candidates = db.query(Candidate).all()

    data = []

    for c in candidates:
        data.append({
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "department": c.department,
            "sub_department": c.sub_department,
            "experience": c.experience,
            "job_role": c.job_role,
            "skills": c.skills,
            "parsed_resume": c.parsed_resume,
            "anonymous_resume": c.anonymous_resume,
            "status": c.status,
        })

    return {
        "success": True,
        "candidates": anonymize_batch(data)
    }


# ── GET /api/resumes/{candidate_id} ──────────────────────────────────────────
@router.get(
    "/{candidate_id}",
    summary="Single anonymized resume",
)
def get_resume(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    c = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not c:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    raw = {
        "id": c.id,
        "name": c.name,
        "email": c.email,
        "phone": c.phone,
        "department": c.department,
        "sub_department": c.sub_department,
        "experience": c.experience,
        "job_role": c.job_role,
        "skills": c.skills,
        "parsed_resume": c.parsed_resume,
        "anonymous_resume": c.anonymous_resume,
        "status": c.status,
    }

    return {
        "success": True,
        "candidate": anonymize_resume(raw)
    }