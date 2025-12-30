import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance.
    Logs are output to both stderr (console) and a file (logs/app.log).
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Check if handlers are already added to avoid duplicates
    if not logger.handlers:
        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Console Handler
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File Handler (Rotating)
        file_handler = RotatingFileHandler(
            LOGS_DIR / "app.log", maxBytes=10*1024*1024, backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
