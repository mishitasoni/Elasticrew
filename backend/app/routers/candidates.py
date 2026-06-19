from http.client import HTTPException

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError


from ..database import get_db
from ..models import Candidate
from ..schemas import CandidateCreate, CandidateResponse, CandidateListResponse

router = APIRouter(prefix="/candidates", tags=["candidates"])


def conflict(detail: str, field: str) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": detail, "field": field},
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_candidate(
    payload: CandidateCreate,
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    # Check for duplicate email
    existing_email = await db.execute(
        select(Candidate).where(Candidate.email == payload.email)
    )
    if existing_email.scalar_one_or_none() is not None:
        return conflict("A candidate with this email already exists.", "email")

    # Check for duplicate phone
    existing_phone = await db.execute(
        select(Candidate).where(Candidate.phone == payload.phone)
    )
    if existing_phone.scalar_one_or_none() is not None:
        return conflict("A candidate with this phone number already exists.", "phone")

    candidate = Candidate(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        experience=payload.experience.value,
        department=payload.department,
        sub_department=payload.sub_department,
        job_role=payload.job_role,
        skills=payload.skills or None,
        resume_file_name=payload.resume_file_name or None,
    )

    db.add(candidate)
    try:
        await db.commit()
        await db.refresh(candidate)
    except IntegrityError as exc:
        await db.rollback()
        msg = str(exc.orig).lower() if exc.orig else ""
        if "email" in msg:
            return conflict("A candidate with this email already exists.", "email")
        if "phone" in msg:
            return conflict("A candidate with this phone number already exists.", "phone")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "A candidate with this information already exists."},
        )

    data = CandidateResponse.model_validate(candidate).model_dump(mode="json")
    return JSONResponse(content=data, status_code=status.HTTP_201_CREATED)


@router.get("", response_model=CandidateListResponse)
async def list_candidates(
    search: str = "",
    department: str = "all",
    sub_department: str = "all",
    stage: str = "all",
    status: str = "all",
    db: AsyncSession = Depends(get_db),
) -> CandidateListResponse:
    query = select(Candidate)

    if search:
        query = query.where(Candidate.full_name.ilike(f"%{search}%"))
    if department and department != "all":
        query = query.where(Candidate.department == department)
    if sub_department and sub_department != "all":
        query = query.where(Candidate.sub_department == sub_department)
    if stage and stage != "all":
        query = query.where(Candidate.stage == stage)
    if status and status != "all":
        query = query.where(Candidate.status == status)

    # Count total matching records
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    # Apply ordering
    query = query.order_by(Candidate.date_added.desc(), Candidate.created_at.desc())

    result = await db.execute(query)
    candidates = result.scalars().all()

    return CandidateListResponse(
        candidates=[CandidateResponse.model_validate(c) for c in candidates],
        total=total,
    )




@router.delete("/{candidate_id}")
async def delete_candidate(
    candidate_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )

    candidate = result.scalar_one_or_none()

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    await db.delete(candidate)
    await db.commit()

    return {
        "success": True,
        "message": "Candidate deleted successfully"
    }