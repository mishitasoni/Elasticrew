from pydantic import BaseModel
from typing import Optional


class CandidateCreate(BaseModel):
    name: str
    email: str
    phone: str
    department: str
    sub_department: str


class CandidateResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    department: str
    sub_department: str

    pipeline_stage: str
    status: str

    resume_filename: Optional[str] = None
    remarks: Optional[str] = None

    class Config:
        from_attributes = True