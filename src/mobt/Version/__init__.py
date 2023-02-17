import logging
import sys

import click

from mobt.Logging import color_by_log_level


class _Formater(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        return click.style(f"{super().format(record)}", fg=color_by_log_level(record))


_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(_Formater())

_logger = logging.getLogger('mobt.Version')
_logger.addHandler(_handler)


def version_checker_thread_logger() -> logging.Logger:
    return _logger
