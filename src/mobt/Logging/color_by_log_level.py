import logging
from logging import LogRecord
from typing import Optional


def color_by_log_level(record: LogRecord) -> str:
    return color_by_log_level_int(record.levelno)


def color_by_log_level_int(level: Optional[int]) -> str:
    """
        Supported color names:

    * ``black`` (might be a gray)
    * ``red``
    * ``green``
    * ``yellow`` (might be an orange)
    * ``blue``
    * ``magenta``
    * ``cyan``
    * ``white`` (might be light gray)
    * ``bright_black``
    * ``bright_red``
    * ``bright_green``
    * ``bright_yellow``
    * ``bright_blue``
    * ``bright_magenta``
    * ``bright_cyan``
    * ``bright_white``
    * ``reset`` (reset the color code only)
    """

    if level == logging.DEBUG:
        return "bright_black"
    elif level == logging.INFO:
        return "white"
    elif level == logging.WARNING:
        return "yellow"
    elif level == logging.ERROR:
        return "red"
    elif level == logging.CRITICAL:
        return "bright_red"
    else:
        return "bright_white"
