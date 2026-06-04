import signal
import sys
from time import sleep

from hypothesis_agent.app.services.analysis_service import complete_analysis
from hypothesis_agent.app.services.job_store import job_store


def run_worker():
    print("[worker] started")
    running = True

    def shutdown(*_args):
        nonlocal running
        running = False
        print("[worker] shutting down")

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    while running:
        try:
            job_id = job_store.dequeue(timeout=5)
            if job_id is None:
                continue

            job = job_store.get(job_id)
            if job is None:
                continue

            print(f"[worker] processing job_id={job_id}")
            complete_analysis(job.query, job_id)
        except KeyboardInterrupt:
            break
        except Exception as exc:
            print(f"[worker] error: {exc!r}")
            sleep(1)

    print("[worker] stopped")


if __name__ == "__main__":
    run_worker()
