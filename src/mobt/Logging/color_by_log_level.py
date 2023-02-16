import logging
from logging import LogRecord


def color_by_log_level(record: LogRecord) -> str:
    level = record.levelno

    if level == logging.DEBUG:
        return "bright_black"
    elif level == logging.INFO:
        return "bright_white"
    elif level == logging.WARNING:
        return "bright_yellow"
    elif level == logging.ERROR:
        return "bright_red"
    elif level == logging.CRITICAL:
        return "bright_red"
    else:
        return "bright_white"
