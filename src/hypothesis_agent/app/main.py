from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hypothesis_agent.app.schemas import QueryRequest
from hypothesis_agent.app.services.analysis_service import run_analysis_pipeline

app = FastAPI(title="Research Reasoning Engine API")

# Allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://research-reasoning-engine.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze(request: QueryRequest):
    result = run_analysis_pipeline(request.query)
    return result
