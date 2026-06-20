from pydantic import BaseModel
from typing import Optional

class CandidateCreate(BaseModel):
    full_name: str
    email: str
    phone: str

    experience: str

    department: str
    sub_department: str

    job_role: str

    skills: Optional[str] = None

    resume_file_name: Optional[str] = None


class CandidateResponse(BaseModel):
    id: int

    full_name: str
    email: str
    phone: str

    experience: str | None = None

    department: str
    sub_department: str

    job_role: str | None = None
    skills: str | None = None

    resume_file_name: str | None = None

    stage: str
    status: str

    remarks: str | None = None

    date_added: str
    created_at: str

    class Config:
        from_attributes = True
class StatusUpdateRequest(BaseModel):
    status: str


class NotesUpdateRequest(BaseModel):
    notes: str


class AddReviewRequest(BaseModel):
    type: str
    reviewer: str
    comment: str