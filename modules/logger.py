import logging
import os

log_filename = os.path.join(os.getcwd(), "muni-transit-display.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(log_filename),  # writes to log file
        logging.StreamHandler(),  # writes to the terminal
    ],
)

logger = logging.getLogger(__name__)
