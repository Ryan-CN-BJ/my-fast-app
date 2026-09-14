from loguru import logger
from userservice.core.config.logConfig import logSetting
from userservice.core.config.webconfig import webSetting
import sys
from pathlib import Path
from dataclasses import dataclass
import time
from enum import StrEnum


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


class LogLevel(StrEnum):
    TRACE = "TRACE"


@dataclass
class LogRecord:
    message: str
    duration_ms: str

    def __post_init__(self):
        self._start_time = time.perf_counter()

    def _emit(self, level: LogLevel, exc: Exception | None) -> None:
        data = self.asdict()
        message = data.pop("message")

        extra = {k: v for k, v in data.items() if v is not None}

        if not extra.get("duration_ms", None):
            extra["duration_ms"] = round(
                (time.perf_counter() - self._start_time) * 1000, 2
            )

        log = logger.bind(**extra) if extra else logger

        if exc:
            log = log.opt(exception=exc)

        getattr(log, level.lower())(message)
