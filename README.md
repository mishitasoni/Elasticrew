# Elasticrew Recruitment Management System

## Overview

Elasticrew is a recruitment management platform designed to streamline candidate hiring workflows. The system enables recruiters to manage candidates, upload resumes, parse resume information, conduct screening processes, manage assessments, and track hiring progress through different pipeline stages.

---

## Features

### Candidate Management

* Add new candidates
* View candidate records
* Manage candidate information
* Department and sub-department assignment

### Resume Upload & Parsing

* Upload resumes (PDF, DOC, DOCX)
* Resume storage and management
* Automatic resume parsing
* Resume metadata extraction
* File type validation
* File size validation

### Recruitment Workflow

* Hiring Queue Management
* Candidate Pipeline Tracking
* Assessment Management
* Department Management
* Reporting Dashboard

### Backend Features

* FastAPI REST APIs
* PostgreSQL Database Integration
* Supabase Cloud Database Support
* SQLAlchemy ORM
* File Upload Handling
* Resume Parsing Services

---

## Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* FastAPI
* SQLAlchemy
* Python

### Database

* PostgreSQL
* Supabase

### Additional Libraries

* PyMuPDF
* python-multipart
* psycopg2
* python-dotenv

---

## Project Structure

```text
ELASTICREW-MAIN
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes/
│   ├── uploads/
│   └── requirements.txt
│
├── all-candidates.html
├── assessments.html
├── client-report.html
├── departments.html
├── hiring-queue.html
├── index.html
├── reports.html
├── style.css
├── tech-scheduler.html
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd ELASTICREW-MAIN
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file inside the backend folder:

```env
DATABASE_URL=your_supabase_connection_string
```

### Run Backend

```bash
cd backend
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Contributors

* Mishita Soni
* Ayushi Pancholi
* Aparna Bhat
* Niharika Singh

---

## License

This project is developed for educational and internship purposes.
