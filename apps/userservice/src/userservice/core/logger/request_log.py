from userservice.core.logger.log_record import LogRecord
from dataclasses import dataclass


@dataclass
class RequestLog(LogRecord):
    method: str = ""
    path: str = ""
    status_code: int = 0
    client_ip: str = ""
