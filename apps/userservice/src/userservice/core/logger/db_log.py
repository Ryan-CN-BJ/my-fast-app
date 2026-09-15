from userservice.core.logger.log_record import LogRecord
from dataclasses import dataclass


@dataclass
class DBLog(LogRecord):
    sql: str = ""
    params: str = ""
