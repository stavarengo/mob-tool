import logging

_loger = logging.getLogger(__name__)


def cache_logger() -> logging.Logger:
    return _loger
