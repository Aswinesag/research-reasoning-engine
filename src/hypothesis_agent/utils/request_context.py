import uuid
import structlog
from structlog.contextvars import bind_contextvars, clear_contextvars

def start_request_context():
    request_id = str(uuid.uuid4())
    bind_contextvars(request_id=request_id)
    return request_id

def clear_request_context():
    clear_contextvars()