"""
Module Name: logger.py
Description: Configures logging for monitoring application runtime. Logs messages at the INFO level and above, with a timestamped format. Logs are saved to a rotating file `app_monitor.log` with a 5 MB size limit and up to 5 backup files, and also output to the console.

Last Updated: 2024-09-01
"""

import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        RotatingFileHandler("app_monitor.log", maxBytes=5 * 1024 * 1024, backupCount=5),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)
