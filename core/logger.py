import logging
import os
from datetime import datetime
from pathlib import Path

# Create logs directory
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Create log file with timestamp
LOG_FILE = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
LOG_FILE_PATH = LOG_DIR / LOG_FILE

# Configure logging
logging.basicConfig(
    filename=str(LOG_FILE_PATH),
    format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("stocksage")
