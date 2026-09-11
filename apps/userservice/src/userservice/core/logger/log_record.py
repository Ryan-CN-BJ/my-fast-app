from loguru import logger
from userservice.core.config.logConfig import logSetting
from userservice.core.config.webconfig import webSetting
import sys
from pathlib import Path


def setLogger() -> None:
    logger.remove()
    if webSetting.environment == "production":
        logger.add(sys.stdout, level=logSetting.level, serialize=True)
    else:
        logger.add(
            sys.stdout,
            level=logSetting.level,
            format="{time}|{level}|{message}|{module}-{line}|{extra}",
        )

    error_log_dir = Path(__file__).parents[7] / "temp"
    error_log_dir.mkdir(parents=True, exist_ok=True)
    logger.add(
        error_log_dir / "errors.log",
        level="ERROR",
        rotation="10 MB",
        retention="7 days",
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | ",
            "{level: <8} | ",
            "{message} | ",
            "{module}-{line} | ",
            "{extra}",
        ),
    )
