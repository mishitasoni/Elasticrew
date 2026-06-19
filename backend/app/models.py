from datetime import date, datetime
from sqlalchemy import Integer, String, Text, Date, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    experience: Mapped[str] = mapped_column(String(50), nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    sub_department: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    job_role: Mapped[str] = mapped_column(String(200), nullable=False)
    skills: Mapped[str | None] = mapped_column(Text, nullable=True)
    resume_file_name: Mapped[str | None] = mapped_column(String(500), nullable=True)
    stage: Mapped[str] = mapped_column(
        String(100), nullable=False, default="Video Screening Pending", index=True
    )
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="Active", index=True
    )
    remarks: Mapped[str] = mapped_column(Text, nullable=False, default="")
    date_added: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
