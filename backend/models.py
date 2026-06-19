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

    


