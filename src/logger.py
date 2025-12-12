from pathlib import Path
from config import config
from logging.config import dictConfig
from logging import getLogger as get_logger

Path("logs").mkdir(parents=True, exist_ok=True)

dictConfig(config.logging)
logger = get_logger(config.docs.title)
