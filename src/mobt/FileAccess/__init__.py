import logging

_logger = logging.getLogger(__name__)


def file_access_logger() -> logging.Logger:
    return _logger
