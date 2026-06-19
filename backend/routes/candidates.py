from utils.resume_parser import extract_text_from_pdf
from utils.anonymiser import anonymize_resume

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    HTTPException
)

from sqlalchemy.orm import Session

from database import get_db
from models import Candidate
from schemas import CandidateCreate, CandidateResponse

import os
import shutil

router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"]
)

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/", response_model=CandidateResponse)
def create_candidate(
    candidate: CandidateCreate,
    db: Session = Depends(get_db)
):
    new_candidate = Candidate(
        name=candidate.full_name,
        email=candidate.email,
        phone=candidate.phone,

        experience=candidate.experience,

        department=candidate.department,
        sub_department=candidate.sub_department,

        job_role=candidate.job_role,
        skills=candidate.skills,

        resume_filename=candidate.resume_file_name,

        pipeline_stage="Resume Uploaded",
        status="Active"
    )

    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return {
    "id": new_candidate.id,
    "full_name": new_candidate.name,
    "email": new_candidate.email,
    "phone": new_candidate.phone,
    "experience": new_candidate.experience,
    "department": new_candidate.department,
    "sub_department": new_candidate.sub_department,
    "job_role": new_candidate.job_role,
    "skills": new_candidate.skills,
    "resume_file_name": new_candidate.resume_filename,
    "stage": new_candidate.pipeline_stage,
    "status": new_candidate.status,
    "remarks": new_candidate.remarks,
    "date_added": new_candidate.created_at.strftime("%Y-%m-%d"),
    "created_at": str(new_candidate.created_at)
}


@router.get("/")
def get_candidates(db: Session = Depends(get_db)):
    candidates = db.query(Candidate).all()

    result = []

    for c in candidates:
        result.append({
            "id": c.id,
            "full_name": c.name,
            "email": c.email,
            "phone": c.phone,
            "experience": c.experience,
            "department": c.department,
            "sub_department": c.sub_department,
            "job_role": c.job_role,
            "skills": c.skills,
            "resume_file_name": c.resume_filename,
            "stage": c.pipeline_stage,
            "status": c.status,
            "remarks": c.remarks,
            "date_added": c.created_at.strftime("%Y-%m-%d"),
            "created_at": str(c.created_at)
        })

    return {
        "candidates": result,
        "total": len(result)
    }

@router.post("/create-with-resume")
async def create_candidate_with_resume(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    department: str = Form(...),
    sub_department: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    allowed_extensions = [
        ".pdf",
        ".doc",
        ".docx"
    ]

    extension = os.path.splitext(
        resume.filename
    )[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOC and DOCX files are allowed"
        )

    contents = await resume.read()

    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="Maximum file size is 5MB"
        )

    await resume.seek(0)

    filepath = os.path.join(
        UPLOAD_DIR,
        resume.filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            resume.file,
            buffer
        )

    parsed_text = extract_text_from_pdf(filepath)

    anonymous_text = anonymize_resume(parsed_text)

    candidate = Candidate(
        name=name,
        email=email,
        phone=phone,

        department=department,
        sub_department=sub_department,

        resume_filename=resume.filename,
        resume_filepath=filepath,

        pipeline_stage="Resume Uploaded",
        status="Active",

        parsed_resume=parsed_text,
        anonymous_resume=anonymous_text
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return {
        "message": "Candidate created successfully",
        "candidate_id": candidate.id,
        "resume_filename": resume.filename,
        "resume_filepath": filepath
    }