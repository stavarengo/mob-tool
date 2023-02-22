import warnings

warnings.filterwarnings('error')

from mobt.PopenObserver import register_popen_wrapper

register_popen_wrapper()

import logging

_logger = logging.getLogger(__name__)


def mob_logger() -> logging.Logger:
    return _logger


from mobt.Logging.logging_utils import get_log_level, setup_logging

setup_logging()


def echo(*args, **kwargs):
    import click
    click.secho(*args, **kwargs)


def prompt(*args, **kwargs):
    if get_log_level() > logging.CRITICAL:
        return ''
    import click
    return click.prompt(*args, **kwargs)
