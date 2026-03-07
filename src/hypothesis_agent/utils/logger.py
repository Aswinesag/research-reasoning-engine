import logging
import structlog
import sys

def setup_logging(environment: str = "dev"):
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    pre_chain = [
        structlog.contextvars.merge_contextvars,
        timestamper,
        structlog.processors.add_log_level,
    ]

    if environment == "dev":
        renderer = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=pre_chain + [
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(level=logging.INFO)