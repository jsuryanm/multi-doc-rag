import os
import logging
from datetime import datetime
import structlog

LOG_DIR = "logs"

logs_dir = os.path.join(os.getcwd(), LOG_DIR)
os.makedirs(logs_dir, exist_ok=True)

log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_file_path = os.path.join(logs_dir, log_file)


def _configure_logger():

    if logging.getLogger().handlers:
        return

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(logging.Formatter("%(message)s"))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(message)s"))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler]
    )

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(
                fmt="iso",
                utc=True,
                key="timestamp"
            ),
            structlog.processors.add_log_level,
            structlog.processors.EventRenamer(to="event"),
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


_configure_logger()

logger = structlog.get_logger("rag_app")