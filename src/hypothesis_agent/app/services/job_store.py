import json
import os
from dataclasses import dataclass, field
from time import time
from typing import Any, Optional
from uuid import uuid4

import redis


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
JOB_QUEUE_KEY = "analysis_job_queue"
JOB_TTL_SECONDS = int(os.getenv("JOB_TTL_SECONDS", "86400"))


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
        self._redis = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        self._prefix = "analysis_job"

    def _key(self, job_id: str) -> str:
        return f"{self._prefix}:{job_id}"

    def _serialize(self, job: AnalysisJob) -> dict[str, Any]:
        return {
            "id": job.id,
            "query": job.query,
            "status": job.status,
            "progress": job.progress,
            "stage": job.stage,
            "created_at": job.created_at,
            "updated_at": job.updated_at,
            "result": json.dumps(job.result) if job.result is not None else "",
            "error": job.error or "",
        }

    def _deserialize(self, payload: dict[str, str]) -> AnalysisJob:
        return AnalysisJob(
            id=payload["id"],
            query=payload["query"],
            status=payload.get("status", "queued"),
            progress=int(payload.get("progress", 0)),
            stage=payload.get("stage", "queued"),
            created_at=float(payload.get("created_at", time())),
            updated_at=float(payload.get("updated_at", time())),
            result=json.loads(payload["result"]) if payload.get("result") else None,
            error=payload.get("error") or None,
        )

    def create(self, query: str) -> AnalysisJob:
        job = AnalysisJob(id=str(uuid4()), query=query)
        self._redis.hset(self._key(job.id), mapping=self._serialize(job))
        self._redis.expire(self._key(job.id), JOB_TTL_SECONDS)
        return job

    def enqueue(self, job_id: str) -> None:
        self._redis.rpush(JOB_QUEUE_KEY, job_id)

    def dequeue(self, timeout: int = 5) -> Optional[str]:
        item = self._redis.blpop(JOB_QUEUE_KEY, timeout=timeout)
        if item is None:
            return None
        _, job_id = item
        return job_id

    def get(self, job_id: str) -> Optional[AnalysisJob]:
        payload = self._redis.hgetall(self._key(job_id))
        if not payload:
            return None
        return self._deserialize(payload)

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
        job = self.get(job_id)
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
        self._redis.hset(self._key(job.id), mapping=self._serialize(job))
        self._redis.expire(self._key(job.id), JOB_TTL_SECONDS)
        return job

job_store = JobStore()
