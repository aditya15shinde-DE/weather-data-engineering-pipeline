from loguru import logger
from pathlib import Path

Path("logs").mkdir(exist_ok=True)

logger.add("logs/pipeline.log",level="INFO",rotation="10 MB")