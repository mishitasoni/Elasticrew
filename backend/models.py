from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    department = Column(String, nullable=False)
    sub_department = Column(String, nullable=False)

    pipeline_stage = Column(String, default="Resume Uploaded")
    status = Column(String, default="Active")

    resume_filename = Column(String, nullable=True)
    remarks = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    resume_filepath = Column(String, nullable=True)

    parsed_resume = Column(String, nullable=True)

    anonymous_resume = Column(String, nullable=True)
    experience = Column(String, nullable=True)

    job_role = Column(String, nullable=True)

    skills = Column(String, nullable=True)
    resume_status = Column(String, default="Awaiting Review")

    hr_notes = Column(String, nullable=True)

    resume_request_date = Column(String, nullable=True)

    resume_submitted_on = Column(String, nullable=True)
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    candidate_id = Column(Integer)

    review_type = Column(String)

    reviewer = Column(String)

    comment = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    


