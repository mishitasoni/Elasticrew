# ElastiCrew — FastAPI Backend

Python 3.14 / FastAPI backend for the ElastiCrew hiring platform.

## Project Structure

```
backend-py/
├── main.py             ← FastAPI app, CORS, static file serving, startup
├── db.py               ← In-memory store + status constants + all CRUD functions
├── anonymizer.py       ← Three-layer PII stripping (field drop → pattern redact → name scrub)
├── models.py           ← Pydantic request/response models (auto-validated by FastAPI)
├── requirements.txt
└── routers/
    ├── resume_queue.py ← /api/resume-queue/** — queue CRUD + status management
    └── resume_view.py  ← /api/resumes/**      — anonymized resume data
```

## Setup

```bash
cd backend-py
pip install -r requirements.txt
```

## Running

```bash
# Development (auto-reload on file save)
uvicorn main:app --reload --port 3000

# Production
uvicorn main:app --host 0.0.0.0 --port 3000 --workers 4
```

Server starts at **http://localhost:3000**

- **Swagger UI** → http://localhost:3000/docs
- **ReDoc**       → http://localhost:3000/redoc

---

## API Reference

### Resume Queue  `/api/resume-queue`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/resume-queue` | Full queue — pending + review queues + KPI stats |
| GET | `/api/resume-queue/stats` | KPI counts only (fast poll, no candidate data) |
| GET | `/api/resume-queue/{id}` | Single anonymized candidate |
| PATCH | `/api/resume-queue/{id}/status` | Update status `{ "status": "..." }` |
| PATCH | `/api/resume-queue/{id}/notes` | Save HR notes `{ "notes": "..." }` |
| POST | `/api/resume-queue/{id}/reviews` | Add review `{ "type", "reviewer", "comment" }` |
| DELETE | `/api/resume-queue/{id}/reviews/{rid}` | Remove a review by UUID |
| PATCH | `/api/resume-queue/{id}/withdraw` | Shortcut to mark Withdrawn |

### Resume View  `/api/resumes`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/resumes` | All anonymized resumes |
| GET | `/api/resumes/{id}` | Single anonymized resume |

### Meta

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/statuses` | All valid status values and pipeline stage labels |

---

## Valid Resume Statuses

```
Upload Pending | Request Sent | Upload Overdue | Incomplete Resume
Awaiting Review | On Hold | Review Completed | Rejected | Withdrawn
```

---

## Anonymization (anonymizer.py)

Three layers applied before any data leaves the server:

| Layer | What it does |
|-------|-------------|
| **1 — Field drop** | Deletes any key in `PII_FIELDS` (name, email, phone, address, DOB, gender, photo, SSN, etc.) |
| **2 — Pattern redact** | Scans every string value with regex — replaces emails, phones, profile URLs, zip codes, SSNs with `[REDACTED]` markers |
| **3 — Name scrub** | Extracts the candidate's own name tokens before stripping, then removes them from all free-text fields (work history, highlights, education) |

---

## Connecting a Real Database

Replace the functions in `db.py` with async DB calls. Signatures stay identical:

```python
# PostgreSQL example with asyncpg
async def get_all_candidates():
    return await conn.fetch("SELECT * FROM candidates")

async def update_resume_status(candidate_id, new_status):
    return await conn.fetchrow(
        "UPDATE candidates SET resume_status=$1 WHERE id=$2 RETURNING *",
        new_status, candidate_id
    )
```
