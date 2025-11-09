import logging
from enum import StrEnum

LOG_FORMAT_DEBUG = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

class LogLevels(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

def configure_logger(log_level: str = LogLevels.ERROR):
    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevels]
    
    if log_level not in log_levels:
        raise ValueError(f"Invalid log level: {log_level}")
    
    if log_level == LogLevels.DEBUG:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
        return
    
    logging.basicConfig(level=log_level)