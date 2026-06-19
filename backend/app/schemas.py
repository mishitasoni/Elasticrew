from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
import re


class ExperienceLevel(str, Enum):
    fresher = "Fresher (0 yrs)"
    junior = "Junior (1\u20133 yrs)"
    mid = "Mid Level (3\u20135 yrs)"
    senior = "Senior (5+ yrs)"
    lead = "Lead (10+ yrs)"


PHONE_RE = re.compile(r"^\+?[\d\s\-()\\.]{7,20}$")


class CandidateCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    experience: ExperienceLevel
    department: str
    sub_department: str
    job_role: str
    skills: str | None = None
    resume_file_name: str | None = None

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Full name must be at least 2 characters.")
        if len(v) > 200:
            raise ValueError("Full name must be at most 200 characters.")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.strip()
        if not PHONE_RE.match(v):
            raise ValueError("Enter a valid phone number (7\u201320 digits).")
        return v

    @field_validator("department")
    @classmethod
    def validate_department(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 1 or len(v) > 100:
            raise ValueError("Department must be 1\u2013100 characters.")
        return v

    @field_validator("sub_department")
    @classmethod
    def validate_sub_department(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 1 or len(v) > 100:
            raise ValueError("Sub department must be 1\u2013100 characters.")
        return v

    @field_validator("job_role")
    @classmethod
    def validate_job_role(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 1 or len(v) > 200:
            raise ValueError("Job role must be 1\u2013200 characters.")
        return v


class CandidateResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    experience: str
    department: str
    sub_department: str
    job_role: str
    skills: str | None
    resume_file_name: str | None
    stage: str
    status: str
    remarks: str
    date_added: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CandidateListResponse(BaseModel):
    candidates: list[CandidateResponse]
    total: int


class ErrorResponse(BaseModel):
    detail: str
    field: str | None = None
