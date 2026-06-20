"""
routers/resume_queue.py
Queue API — all CRUD operations on the resume review queue.

Prefix : /api/resume-queue
Tags   : Resume Queue
"""

from __future__ import annotations
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from fastapi import Depends

from database import get_db
from models import Candidate, Review
from schemas import (
    StatusUpdateRequest,
    NotesUpdateRequest,
    AddReviewRequest
)

from anonymizer import anonymize_resume, anonymize_batch

router = APIRouter(prefix="/api/resume-queue", tags=["Resume Queue"])

# ── Pending statuses (not yet submitted / incomplete) ─────────────────────────

_PENDING = {
    "Upload Pending",
    "Request Sent",
    "Upload Overdue",
    "Incomplete"
}


def _not_found(candidate_id: str) -> HTTPException:
    return HTTPException(status_code=404, detail=f"Candidate {candidate_id} not found")


def _bad_request(msg: str) -> HTTPException:
    return HTTPException(status_code=400, detail=msg)


# ── GET /api/resume-queue ─────────────────────────────────────────────────────
@router.get("")
def get_resume_queue(
    db: Session = Depends(get_db)
):
    candidates = db.query(Candidate).all()

    all_candidates = []

    for c in candidates:
        all_candidates.append({
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "department": c.department,
            "sub_department": c.sub_department,
            "experience": c.experience,
            "job_role": c.job_role,
            "skills": c.skills,
            "resume_status": c.resume_status,
            "status": c.status,
            "anonymous_resume": c.anonymous_resume,
            "parsed_resume": c.parsed_resume,
        })

    pending = [
        c for c in all_candidates
        if c["resume_status"] in _PENDING
    ]

    review = [
        c for c in all_candidates
        if c["resume_status"] not in _PENDING
    ]

    return {
        "success": True,
        "pending_queue": anonymize_batch(pending),
        "review_queue": anonymize_batch(review),
        "stats": {
            "pending": len(pending),
            "review": len(review)
        }
    }


# ── GET /api/resume-queue/stats ───────────────────────────────────────────────
@router.get(
    "/stats",
    summary="KPI stats only",
    description="Returns status counts without candidate payloads — fast for polling.",
)
def get_queue_stats():
    return {"success": True, "stats": db.get_queue_stats()}


# ── GET /api/resume-queue/{candidate_id} ─────────────────────────────────────
@router.get(
    "/{candidate_id}",
    summary="Single anonymized candidate",
)
def get_candidate(candidate_id: str):
    raw = db.get_candidate_by_id(candidate_id)
    if raw is None:
        raise _not_found(candidate_id)
    return {"success": True, "candidate": anonymize_resume(raw)}


# ── PATCH /api/resume-queue/{candidate_id}/status ────────────────────────────
@router.patch(
    "/{candidate_id}/status",
    summary="Update resume queue status",
    description='Body: `{ "status": "Awaiting Review" }`',
)
def update_status(candidate_id: str, body: StatusUpdateRequest):
    try:
        updated = db.update_resume_status(candidate_id, body.status)
    except KeyError as e:
        raise _not_found(candidate_id) from e
    except ValueError as e:
        raise _bad_request(str(e)) from e
    return {"success": True, "candidate": anonymize_resume(updated)}


# ── PATCH /api/resume-queue/{candidate_id}/notes ─────────────────────────────
@router.patch(
    "/{candidate_id}/notes",
    summary="Save HR notes",
    description='Body: `{ "notes": "..." }`',
)
def save_notes(candidate_id: str, body: NotesUpdateRequest):
    try:
        result = db.save_hr_notes(candidate_id, body.notes)
    except KeyError as e:
        raise _not_found(candidate_id) from e
    return {"success": True, **result}


# ── POST /api/resume-queue/{candidate_id}/reviews ────────────────────────────
@router.post(
    "/{candidate_id}/reviews",
    status_code=status.HTTP_201_CREATED,
    summary="Add a review comment",
    description='Body: `{ "type": "screening"|"interview", "reviewer": "...", "comment": "..." }`',
)
def add_review(candidate_id: str, body: AddReviewRequest):
    try:
        entry = db.add_review(candidate_id, body.type, body.reviewer, body.comment)
    except KeyError as e:
        raise _not_found(candidate_id) from e
    except ValueError as e:
        raise _bad_request(str(e)) from e
    return {"success": True, "review": entry}


# ── DELETE /api/resume-queue/{candidate_id}/reviews/{review_id} ──────────────
@router.delete(
    "/{candidate_id}/reviews/{review_id}",
    summary="Remove a review entry",
)
def remove_review(candidate_id: str, review_id: str):
    try:
        result = db.remove_review(candidate_id, review_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return {"success": True, **result}


# ── PATCH /api/resume-queue/{candidate_id}/withdraw ──────────────────────────
@router.patch(
    "/{candidate_id}/withdraw",
    summary="Withdraw a candidate",
    description="Convenience shortcut — sets status to Withdrawn.",
)
def withdraw_candidate(candidate_id: str):
    try:
        updated = db.update_resume_status(candidate_id, db.ResumeStatus.WITHDRAWN)
    except KeyError as e:
        raise _not_found(candidate_id) from e
    return {"success": True, "candidate": anonymize_resume(updated)}
