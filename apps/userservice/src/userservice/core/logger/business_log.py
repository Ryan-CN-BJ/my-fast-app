from userservice.core.logger.log_record import LogRecord
from dataclasses import dataclass
from collections.abc import Callable
from typing import Any
from functools import wraps


@dataclass
class BusinessLog(LogRecord):
    action: str
    entity: str
    entity_id: str


EntityIdExtractor = Callable[[tuple, dict[str, Any], Any], str | int]


def service_logger(action: str, entity: str, id_extractor: EntityIdExtractor | None):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        async def wrapper(*args: Any, **kw: Any):
            log = BusinessLog(message="", action=action, entity=entity)
            try:
                result = await func(*args, **kw)
                if id_extractor:
                    log.entity_id = id_extractor(args, kw, result)
                log.message = f"{action}成功"
                log.success()
                return result
            except Exception as e:
                if id_extractor:
                    log.entity_id = id_extractor(args, kw, None)
                log.message = f"{action}失败"
                log.warning()

        return wrapper

    return decorator
