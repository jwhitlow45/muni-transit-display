import logging
import os

from modules.environment import LOG_LEVEL

log_filename = os.path.join(os.getcwd(), "transit-display.log")


log_level = LOG_LEVEL.upper() or logging.INFO

logging.basicConfig(
    level=log_level,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(log_filename),  # writes to log file
        logging.StreamHandler(),  # writes to the terminal
    ],
)

logger = logging.getLogger(__name__)
