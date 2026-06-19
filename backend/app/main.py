from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import candidates

app = FastAPI(
    title="ElastiCrew ATS API",
    version="1.0.0",
    description="Applicant Tracking System REST API for ElastiCrew",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidates.router, prefix="/api")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
