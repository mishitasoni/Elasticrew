# ElastiCrew — Migration: React + FastAPI + PostgreSQL

## Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 15+ running locally

---

## Step 1: Database Setup

Create the database:
```bash
createdb elasticrew
```

---

## Step 2: Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

Create a `.env` file in `backend/`:
```
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/elasticrew
```

Run migrations (creates table + seeds 6 existing candidates):
```bash
alembic upgrade head
```

Start the API server:
```bash
uvicorn app.main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

---

## Step 3: Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

The Vite dev server proxies `/api/*` requests to `http://localhost:8000`, so no CORS issues during development.

---

## API Endpoints

| Method | Path            | Description                            |
|--------|-----------------|----------------------------------------|
| GET    | /api/candidates | List candidates with optional filters  |
| POST   | /api/candidates | Create a new candidate (201 Created)   |
| GET    | /health         | Health check                           |

### GET /api/candidates — Query Parameters

| Parameter      | Default | Description                         |
|----------------|---------|-------------------------------------|
| search         | ""      | ILIKE filter on full_name           |
| department     | "all"   | Exact match on department           |
| sub_department | "all"   | Exact match on sub_department       |
| stage          | "all"   | Exact match on stage                |
| status         | "all"   | Exact match on status               |

### POST /api/candidates — Request Body

```json
{
  "full_name": "Jane Doe",
  "email": "jane@company.com",
  "phone": "+91 9876543210",
  "experience": "Junior (1–3 yrs)",
  "department": "Engineering",
  "sub_department": "Backend",
  "job_role": "Backend Engineer",
  "skills": "Python, FastAPI",
  "resume_file_name": "jane_resume.pdf"
}
```

**Responses:**
- `201 Created` — Candidate created successfully
- `409 Conflict` — `{"detail": "A candidate with this email already exists.", "field": "email"}`
- `422 Unprocessable Entity` — Pydantic validation errors

---

## Database Schema

See `backend/alembic/versions/0001_create_candidates_table.py`

```sql
CREATE TABLE candidates (
    id              SERIAL PRIMARY KEY,
    full_name       VARCHAR(200)  NOT NULL,
    email           VARCHAR(320)  NOT NULL UNIQUE,
    phone           VARCHAR(30)   NOT NULL UNIQUE,
    experience      VARCHAR(50)   NOT NULL,
    department      VARCHAR(100)  NOT NULL,
    sub_department  VARCHAR(100)  NOT NULL,
    job_role        VARCHAR(200)  NOT NULL,
    skills          TEXT,
    resume_file_name VARCHAR(500),
    stage           VARCHAR(100)  NOT NULL DEFAULT 'Video Screening Pending',
    status          VARCHAR(50)   NOT NULL DEFAULT 'Active',
    remarks         TEXT          DEFAULT '',
    date_added      DATE          NOT NULL DEFAULT CURRENT_DATE,
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);
```

---

## Project Structure

```
Elasticrew-main/
  backend/
    app/
      __init__.py
      main.py          — FastAPI app + CORS
      database.py      — Async SQLAlchemy engine + get_db
      models.py        — Candidate ORM model
      schemas.py       — Pydantic v2 schemas
      routers/
        __init__.py
        candidates.py  — GET + POST /api/candidates
    requirements.txt
    alembic.ini
    alembic/
      env.py
      versions/
        0001_create_candidates_table.py   — Table creation + seed data
  frontend/
    package.json
    vite.config.ts
    tsconfig.json
    index.html
    src/
      main.tsx
      App.tsx
      api/
        candidatesApi.ts
      components/
        candidates/
          CandidatesPage.tsx    — Full page with sidebar
          CandidateTable.tsx    — Table + skeleton loader
          CandidateRow.tsx      — Individual table row
          AddCandidateModal.tsx — 9-field add form modal
        ui/
          Toast.tsx             — Animated success toast
      hooks/
        useCandidates.ts        — Data fetching + filtering state
        useAddCandidate.ts      — Form state + validation + submission
      types/
        candidate.ts            — All TypeScript interfaces/types
      styles/
        global.css              — Full design system (matches style.css)
  Elasticrew-main/             — Original HTML/CSS/JS frontend
  MIGRATION.md                 — This file
```

---

## Notes

- The React app is a full-page replacement for `all-candidates.html`. Sidebar links point back to the original HTML pages for other sections.
- No CSS framework is used — all styling comes from the `global.css` that mirrors the existing `style.css` design system (Outfit font, navy blue `#0E2D7B`, Glassmorphism modals).
- Status and action dropdowns in the table currently update client-side styling only. A `PATCH /api/candidates/:id` endpoint would be needed to persist those changes.
