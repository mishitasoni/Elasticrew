"""
db.py
In-memory data store — simulates a database for candidates and queue state.

Replace the dict/list operations here with real async DB calls
(e.g. asyncpg for PostgreSQL, motor for MongoDB) when connecting to a
live database. The public function signatures stay identical.
"""

from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Optional
from copy import deepcopy

# ── VALID QUEUE STATUSES ──────────────────────────────────────────────────────
class ResumeStatus:
    UPLOAD_PENDING   = "Upload Pending"
    REQUEST_SENT     = "Request Sent"
    UPLOAD_OVERDUE   = "Upload Overdue"
    INCOMPLETE       = "Incomplete Resume"
    AWAITING_REVIEW  = "Awaiting Review"
    ON_HOLD          = "On Hold"
    REVIEW_COMPLETED = "Review Completed"
    REJECTED         = "Rejected"
    WITHDRAWN        = "Withdrawn"

    @classmethod
    def all_values(cls) -> list[str]:
        return [
            cls.UPLOAD_PENDING, cls.REQUEST_SENT, cls.UPLOAD_OVERDUE,
            cls.INCOMPLETE, cls.AWAITING_REVIEW, cls.ON_HOLD,
            cls.REVIEW_COMPLETED, cls.REJECTED, cls.WITHDRAWN,
        ]

PIPELINE_STAGES = [
    "Video Bot Screening",
    "Resume Review",
    "MCQ Assessment",
    "Tech Scheduler",
    "HR Interview",
]

# ── SEED DATA ─────────────────────────────────────────────────────────────────
# Raw records include PII — anonymizer strips it before client delivery.
_candidates: list[dict] = [
    {
        "id": "C-1021",
        "name": "Grace Hopper",
        "email": "grace.hopper@example.com",
        "phone": "+1-555-000-0001",
        "role": "Software Engineer",
        "dept": "Engineering",
        "subdept": "Full Stack",
        "exp": "Senior (5+ Y)",
        "date_applied": "2026-06-08",
        "admin_status": "Active",
        "resume_status": ResumeStatus.AWAITING_REVIEW,
        "resume_submitted_on": "2026-06-03",
        "resume_request_date": "2026-06-01",
        "tech_stack": ["Python", "Django", "FastAPI", "PostgreSQL", "AWS", "Docker", "Redis", "Celery"],
        "highlights": [
            "Well-structured, modular document architecture across all submissions",
            "Strong backend and distributed systems engineering depth",
            "Relevant microservices and async pipeline background",
            "Clear project ownership and system-level reasoning",
        ],
        "education": "B.S. Computer Science — Distributed Systems & Backend Architecture. Graduated 2019.",
        "work_history": [
            {
                "title": "Senior Software Engineer",
                "org": "Tech Solutions Inc.",
                "period": "2021 – Present",
                "body": "Architected async microservices pipelines processing concurrent request loads at scale.",
            },
            {
                "title": "Backend Engineer",
                "org": "CloudBase Systems",
                "period": "2019 – 2021",
                "body": "Built REST and GraphQL API layers with Django and FastAPI.",
            },
        ],
        "pipeline_stages": [
            {"label": "Video Bot Screening", "done": True},
            {"label": "Resume Review",       "done": False},
            {"label": "MCQ Assessment",      "done": False},
            {"label": "Tech Scheduler",      "done": False},
            {"label": "HR Interview",        "done": False},
        ],
        "screening_reviews": [
            {
                "id": str(uuid.uuid4()),
                "reviewer": "HR Reviewer",
                "comment": "Strong communication and confident delivery.",
                "added_at": "2026-06-04T09:00:00+00:00",
            }
        ],
        "interview_reviews": [],
        "hr_notes": "",
    },
    {
        "id": "C-1025",
        "name": "Charles Babbage",
        "email": "charles.babbage@example.com",
        "phone": "+1-555-000-0002",
        "role": "Hardware Engineer",
        "dept": "Engineering",
        "subdept": "Hardware",
        "exp": "Mid Level (3-5 Y)",
        "date_applied": "2026-05-28",
        "admin_status": "Active",
        "resume_status": ResumeStatus.REVIEW_COMPLETED,
        "resume_submitted_on": "2026-05-30",
        "resume_request_date": "2026-05-28",
        "tech_stack": ["C++", "VHDL", "Embedded C", "Linux", "ARM", "SPI/I2C"],
        "highlights": [
            "FPGA prototyping and firmware development",
            "Strong hardware-software co-design background",
        ],
        "education": "B.S. Electrical Engineering — Computer Architecture. Graduated 2020.",
        "work_history": [
            {
                "title": "Hardware Engineer",
                "org": "Chip Design Co.",
                "period": "2020 – Present",
                "body": "FPGA prototyping and firmware development for embedded sensor platforms.",
            }
        ],
        "pipeline_stages": [
            {"label": "Video Bot Screening", "done": True},
            {"label": "Resume Review",       "done": True},
            {"label": "MCQ Assessment",      "done": False},
            {"label": "Tech Scheduler",      "done": False},
            {"label": "HR Interview",        "done": False},
        ],
        "screening_reviews": [],
        "interview_reviews": [],
        "hr_notes": "",
    },
    {
        "id": "C-1029",
        "name": "Linus Torvalds",
        "email": "linus.t@example.com",
        "phone": "+1-555-000-0003",
        "role": "Product Lead",
        "dept": "Product",
        "subdept": "Product",
        "exp": "Senior (5+ Y)",
        "date_applied": "2026-05-25",
        "admin_status": "Active",
        "resume_status": ResumeStatus.AWAITING_REVIEW,
        "resume_submitted_on": "2026-05-25",
        "resume_request_date": "2026-05-25",
        "tech_stack": ["Linux Kernel", "C", "Git", "JIRA", "Confluence", "Agile"],
        "highlights": [
            "Led cross-functional teams shipping 3 major platform releases",
            "Reduced bug backlog by 60% through process improvements",
        ],
        "education": "B.S. Computer Science — Operating Systems. Graduated 2017.",
        "work_history": [
            {
                "title": "Product Lead",
                "org": "Open Source Ventures",
                "period": "2019 – Present",
                "body": "Led cross-functional product teams, managed roadmap and stakeholder communications.",
            }
        ],
        "pipeline_stages": [
            {"label": "Video Bot Screening", "done": True},
            {"label": "Resume Review",       "done": False},
            {"label": "MCQ Assessment",      "done": False},
            {"label": "Tech Scheduler",      "done": False},
            {"label": "HR Interview",        "done": False},
        ],
        "screening_reviews": [],
        "interview_reviews": [],
        "hr_notes": "",
    },
    {
        "id": "C-1033",
        "name": "Tim Berners-Lee",
        "email": "tim.bl@example.com",
        "phone": "+1-555-000-0004",
        "role": "Full Stack Engineer",
        "dept": "Engineering",
        "subdept": "Full Stack",
        "exp": "Mid Level (3-5 Y)",
        "date_applied": "2026-05-18",
        "admin_status": "Active",
        "resume_status": ResumeStatus.ON_HOLD,
        "resume_submitted_on": "2026-05-20",
        "resume_request_date": "2026-05-18",
        "tech_stack": ["React", "Node.js", "TypeScript", "HTML", "CSS", "REST APIs", "Docker"],
        "highlights": [
            "Built scalable web apps serving 500K+ monthly users",
            "Strong full-stack integration across frontend and backend layers",
        ],
        "education": "M.S. Computer Science — Web Systems. Graduated 2021.",
        "work_history": [
            {
                "title": "Full Stack Engineer",
                "org": "WebCraft Ltd.",
                "period": "2021 – Present",
                "body": "Built scalable web apps serving 500K+ monthly users.",
            }
        ],
        "pipeline_stages": [
            {"label": "Video Bot Screening", "done": True},
            {"label": "Resume Review",       "done": False},
            {"label": "MCQ Assessment",      "done": False},
            {"label": "Tech Scheduler",      "done": False},
            {"label": "HR Interview",        "done": False},
        ],
        "screening_reviews": [],
        "interview_reviews": [],
        "hr_notes": "Pending background check clarification.",
    },
    {
        "id": "C-1042",
        "name": "Alan Turing",
        "email": "alan.turing@example.com",
        "phone": "+1-555-000-0005",
        "role": "Backend Engineer",
        "dept": "Engineering",
        "subdept": "Backend",
        "exp": "Senior (5+ Y)",
        "date_applied": "2026-06-10",
        "admin_status": "Active",
        "resume_status": ResumeStatus.UPLOAD_PENDING,
        "resume_submitted_on": None,
        "resume_request_date": None,
        "tech_stack": ["Python", "Go", "PostgreSQL", "Kafka", "Docker", "Kubernetes"],
        "highlights": ["Distributed systems expert", "Strong theoretical CS background"],
        "education": "Ph.D. Mathematics — Computability Theory. Graduated 1938.",
        "work_history": [],
        "pipeline_stages": [
            {"label": "Video Bot Screening", "done": False},
            {"label": "Resume Review",       "done": False},
            {"label": "MCQ Assessment",      "done": False},
            {"label": "Tech Scheduler",      "done": False},
            {"label": "HR Interview",        "done": False},
        ],
        "screening_reviews": [],
        "interview_reviews": [],
        "hr_notes": "",
    },
    {
        "id": "C-1045",
        "name": "Ada Lovelace",
        "email": "ada.lovelace@example.com",
        "phone": "+1-555-000-0006",
        "role": "Frontend Engineer",
        "dept": "Engineering",
        "subdept": "Frontend",
        "exp": "Junior (1-3 Y)",
        "date_applied": "2026-06-01",
        "admin_status": "Active",
        "resume_status": ResumeStatus.UPLOAD_OVERDUE,
        "resume_submitted_on": None,
        "resume_request_date": "2026-06-02",
        "tech_stack": ["HTML", "CSS", "JavaScript", "React", "Figma"],
        "highlights": ["Accessibility-first development", "Strong visual design sensibility"],
        "education": "B.Des. Interaction Design — HCI. Graduated 2024.",
        "work_history": [],
        "pipeline_stages": [
            {"label": "Video Bot Screening", "done": False},
            {"label": "Resume Review",       "done": False},
            {"label": "MCQ Assessment",      "done": False},
            {"label": "Tech Scheduler",      "done": False},
            {"label": "HR Interview",        "done": False},
        ],
        "screening_reviews": [],
        "interview_reviews": [],
        "hr_notes": "",
    },
    {
        "id": "C-1048",
        "name": "Margaret Hamilton",
        "email": "margaret.hamilton@example.com",
        "phone": "+1-555-000-0007",
        "role": "Systems Engineer",
        "dept": "Engineering",
        "subdept": "Systems Eng",
        "exp": "Senior (5+ Y)",
        "date_applied": "2026-06-11",
        "admin_status": "Active",
        "resume_status": ResumeStatus.REQUEST_SENT,
        "resume_submitted_on": None,
        "resume_request_date": "2026-06-11",
        "tech_stack": ["C++", "Python", "Linux", "Embedded Systems", "RTOS", "TCP/IP"],
        "highlights": ["Deep embedded programming experience", "Flight-critical software background"],
        "education": "B.S. Electrical & Computer Engineering — Embedded Systems. Graduated 2020.",
        "work_history": [],
        "pipeline_stages": [
            {"label": "Video Bot Screening", "done": False},
            {"label": "Resume Review",       "done": False},
            {"label": "MCQ Assessment",      "done": False},
            {"label": "Tech Scheduler",      "done": False},
            {"label": "HR Interview",        "done": False},
        ],
        "screening_reviews": [],
        "interview_reviews": [],
        "hr_notes": "",
    },
    {
        "id": "C-1051",
        "name": "John von Neumann",
        "email": "john.neumann@example.com",
        "phone": "+1-555-000-0008",
        "role": "Data Scientist",
        "dept": "Data",
        "subdept": "Data Science",
        "exp": "Mid Level (3-5 Y)",
        "date_applied": "2026-06-09",
        "admin_status": "Active",
        "resume_status": ResumeStatus.INCOMPLETE,
        "resume_submitted_on": "2026-06-12",
        "resume_request_date": "2026-06-09",
        "tech_stack": ["Python", "R", "TensorFlow", "PyTorch", "SQL", "Spark"],
        "highlights": ["Strong mathematical and statistical modelling background"],
        "education": "Ph.D. Mathematics — Game Theory & Statistics. Graduated 1926.",
        "work_history": [],
        "pipeline_stages": [
            {"label": "Video Bot Screening", "done": False},
            {"label": "Resume Review",       "done": False},
            {"label": "MCQ Assessment",      "done": False},
            {"label": "Tech Scheduler",      "done": False},
            {"label": "HR Interview",        "done": False},
        ],
        "screening_reviews": [],
        "interview_reviews": [],
        "hr_notes": "Missing work history section.",
    },
]

# O(1) lookup map
_candidate_map: dict[str, dict] = {c["id"]: c for c in _candidates}


# ── PUBLIC STORE FUNCTIONS ────────────────────────────────────────────────────

def get_all_candidates() -> list[dict]:
    """Return shallow copies of all candidate records (PII intact — use anonymizer)."""
    return [deepcopy(c) for c in _candidates]


def get_candidate_by_id(candidate_id: str) -> Optional[dict]:
    """Return a copy of a single candidate or None if not found."""
    c = _candidate_map.get(candidate_id)
    return deepcopy(c) if c else None


def update_resume_status(candidate_id: str, new_status: str) -> dict:
    """
    Set a candidate's resume_status.
    Auto-marks the 'Resume Review' pipeline stage done when status = Review Completed.
    Raises ValueError for invalid status or KeyError for unknown id.
    """
    if new_status not in ResumeStatus.all_values():
        raise ValueError(f'Invalid status: "{new_status}"')
    c = _candidate_map.get(candidate_id)
    if c is None:
        raise KeyError(f"Candidate {candidate_id} not found")
    c["resume_status"] = new_status
    if new_status == ResumeStatus.REVIEW_COMPLETED:
        for stage in c["pipeline_stages"]:
            if stage["label"] == "Resume Review":
                stage["done"] = True
    return deepcopy(c)


def save_hr_notes(candidate_id: str, notes: str) -> dict:
    """Save HR notes. Returns {id, hr_notes}."""
    c = _candidate_map.get(candidate_id)
    if c is None:
        raise KeyError(f"Candidate {candidate_id} not found")
    c["hr_notes"] = notes.strip()
    return {"id": c["id"], "hr_notes": c["hr_notes"]}


def add_review(candidate_id: str, review_type: str, reviewer: str, comment: str) -> dict:
    """
    Append a review entry to screening_reviews or interview_reviews.
    review_type must be 'screening' or 'interview'.
    Returns the new entry dict.
    """
    if review_type not in ("screening", "interview"):
        raise ValueError(f'Invalid review type: "{review_type}". Must be "screening" or "interview"')
    c = _candidate_map.get(candidate_id)
    if c is None:
        raise KeyError(f"Candidate {candidate_id} not found")
    entry = {
        "id":       str(uuid.uuid4()),
        "reviewer": reviewer.strip(),
        "comment":  comment.strip(),
        "added_at": datetime.now(timezone.utc).isoformat(),
    }
    field = "screening_reviews" if review_type == "screening" else "interview_reviews"
    c[field].append(entry)
    return deepcopy(entry)


def remove_review(candidate_id: str, review_id: str) -> dict:
    """
    Remove a review entry by UUID from either reviews list.
    Returns {id, removed_from} or raises KeyError if not found.
    """
    c = _candidate_map.get(candidate_id)
    if c is None:
        raise KeyError(f"Candidate {candidate_id} not found")
    for field in ("screening_reviews", "interview_reviews"):
        for i, r in enumerate(c[field]):
            if r["id"] == review_id:
                c[field].pop(i)
                return {"id": review_id, "removed_from": field}
    raise KeyError(f"Review {review_id} not found for candidate {candidate_id}")


def get_queue_stats() -> dict[str, int]:
    """Return count of candidates per status."""
    counts: dict[str, int] = {s: 0 for s in ResumeStatus.all_values()}
    for c in _candidates:
        counts[c["resume_status"]] = counts.get(c["resume_status"], 0) + 1
    return counts
