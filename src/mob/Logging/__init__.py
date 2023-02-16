import logging

import click

from mob.Logging.color_by_log_level import color_by_log_level


class _Formater(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        return click.style(f"{super().format(record)}", fg=color_by_log_level(record))


_handler = logging.StreamHandler()
_handler.setFormatter(_Formater())

_logger = logging.getLogger('mob')
_logger.addHandler(_handler)


def mob_logger() -> logging.Logger:
    return _logger
