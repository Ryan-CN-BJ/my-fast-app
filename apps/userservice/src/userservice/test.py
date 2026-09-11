from loguru import logger
from pathlib import Path
import sys

alllog = Path(__file__).parent / "test.log"

errorlog = Path(__file__).parent / "error.log"

logger.remove()

logger.add(alllog, level="ERROR")
logger.add(
    errorlog,
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss}|{level}|{message}|{module}-{line}|{extra}",
)

logger.add(sys.stdout, level="ERROR")

logger.info("你好")
logger.bind(a=1, b=2).error("出错了")
