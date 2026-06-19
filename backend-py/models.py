"""
models.py
Pydantic request and response models for the ElastiCrew API.
FastAPI uses these for automatic validation, serialisation, and Swagger docs.
"""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


# ── Request bodies ────────────────────────────────────────────────────────────

class StatusUpdateRequest(BaseModel):
    status: str = Field(..., min_length=1, max_length=100, description="New resume queue status")


class NotesUpdateRequest(BaseModel):
    notes: str = Field(..., max_length=5000, description="HR notes text (empty string to clear)")


class AddReviewRequest(BaseModel):
    type: str     = Field(..., pattern="^(screening|interview)$", description="'screening' or 'interview'")
    reviewer: str = Field(..., min_length=1, max_length=200)
    comment: str  = Field(..., min_length=1, max_length=5000)


# ── Response shapes ───────────────────────────────────────────────────────────

class ReviewEntry(BaseModel):
    id: str
    reviewer: str
    comment: str
    added_at: str


class PipelineStage(BaseModel):
    label: str
    done: bool


class CandidateOut(BaseModel):
    """Anonymized candidate record — no PII fields present."""
    id: str
    role: str
    dept: str
    subdept: str
    exp: str
    date_applied: str
    admin_status: str
    resume_status: str
    resume_submitted_on: Optional[str]
    resume_request_date: Optional[str]
    tech_stack: list[str]
    highlights: list[str]
    education: str
    work_history: list[dict]
    pipeline_stages: list[PipelineStage]
    screening_reviews: list[ReviewEntry]
    interview_reviews: list[ReviewEntry]
    # metadata
    anonymized: bool
    anonymized_at: str


class QueueStatsOut(BaseModel):
    """KPI counts keyed by status label."""
    stats: dict[str, int]
