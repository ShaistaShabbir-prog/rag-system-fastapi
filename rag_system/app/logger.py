from loguru import logger
from pathlib import Path

# Log file path
log_file = Path("logs/app.log")

# Configure Loguru
logger.add(log_file, rotation="1 MB", retention="7 days", level="INFO")

logger.info("Logger initialized successfully")
