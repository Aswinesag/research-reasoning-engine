from dataclasses import dataclass, field
from threading import Lock
from time import time
from typing import Any, Optional
from uuid import uuid4


@dataclass
class AnalysisJob:
    id: str
    query: str
    status: str = "queued"
    progress: int = 0
    stage: str = "queued"
    created_at: float = field(default_factory=time)
    updated_at: float = field(default_factory=time)
    result: Optional[dict[str, Any]] = None
    error: Optional[str] = None


class JobStore:
    def __init__(self):
        self._jobs: dict[str, AnalysisJob] = {}
        self._lock = Lock()

    def create(self, query: str) -> AnalysisJob:
        job = AnalysisJob(id=str(uuid4()), query=query)
        with self._lock:
            self._jobs[job.id] = job
        return job

    def get(self, job_id: str) -> Optional[AnalysisJob]:
        with self._lock:
            return self._jobs.get(job_id)

    def update(
        self,
        job_id: str,
        *,
        status: Optional[str] = None,
        progress: Optional[int] = None,
        stage: Optional[str] = None,
        result: Optional[dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> Optional[AnalysisJob]:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return None
            if status is not None:
                job.status = status
            if progress is not None:
                job.progress = progress
            if stage is not None:
                job.stage = stage
            if result is not None:
                job.result = result
            if error is not None:
                job.error = error
            job.updated_at = time()
            return job


job_store = JobStore()
