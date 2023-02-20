import logging

from .cli import cli

_logger = logging.getLogger(__name__)


def controllers_logger() -> logging.Logger:
    return _logger
