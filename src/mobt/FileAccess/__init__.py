import logging

_logger = logging.getLogger('mobt.FileAccess')


def file_access_logger() -> logging.Logger:
    return _logger
