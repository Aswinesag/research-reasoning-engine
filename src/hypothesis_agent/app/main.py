from fastapi import FastAPI
from fastapi import BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

from hypothesis_agent.app.schemas import QueryRequest
from hypothesis_agent.app.services.analysis_service import (
    build_fast_analysis,
    complete_analysis,
    get_job_result,
)

app = FastAPI(title="Research Reasoning Engine API")

frontend_origin = os.getenv("FRONTEND_ORIGIN", "https://research-reasoning-engine.vercel.app")

# Allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        frontend_origin,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze(request: QueryRequest, background_tasks: BackgroundTasks):
    result = build_fast_analysis(request.query)
    job_id = result.get("job_id")
    if job_id:
        background_tasks.add_task(complete_analysis, request.query, job_id)
    return result


@app.get("/results/{job_id}")
async def get_result(job_id: str):
    result = get_job_result(job_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return result
