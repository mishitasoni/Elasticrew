from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import engine
from models import Base

from routes.candidates import router as candidate_router
from routes.resume import router as resume_router


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Elasticrew API"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(candidate_router)
app.include_router(resume_router)

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="../"), name="static")


# Homepage
@app.get("/")
def home():
    return FileResponse("../index.html")


# Optional route for All Candidates page
@app.get("/all-candidates")
def all_candidates():
    return FileResponse("../all-candidates.html")


# Health check
@app.get("/api")
def api_status():
    return {
        "message": "Elasticrew Backend Running"
    }