import logging

import click

from mob.Controllers.boostrap_cli_app import bootstrap_cli_app
from mob.Controllers.done import done
from mob.Controllers.next import next
from mob.Controllers.start import start
from mob.DotEnv.DotEnv import DotEnv
from mob.di import di

_dotEnt = di.get(DotEnv)


@click.group()
@click.version_option(package_name=_dotEnt.PYPI_APP_NAME)
@click.option('-v', '--verbose', count=True,
              help='Enables verbose mode. The more -v options, the more verbose, up to -vvv')
@click.option('-s', '--silent', count=True,
              help='Disable all output except errors. To disable errors, use -ss')
def cli(verbose, silent):
    mob_logger_level = logging.WARNING
    git_logger_level = logging.INFO
    version_checker_thread_logger_level = logging.NOTSET

    if silent == 1:
        mob_logger_level = logging.ERROR
        git_logger_level = logging.ERROR
        version_checker_thread_logger_level = logging.ERROR
    elif silent >= 2:
        mob_logger_level = logging.NOTSET
        git_logger_level = logging.NOTSET
        version_checker_thread_logger_level = logging.NOTSET
    elif verbose == 0:
        # Default value set before the if
        pass
    elif verbose == 1:
        mob_logger_level = logging.INFO
        git_logger_level = logging.INFO
        version_checker_thread_logger_level = logging.WARNING
    elif verbose == 2:
        mob_logger_level = logging.INFO
        git_logger_level = logging.DEBUG
        version_checker_thread_logger_level = logging.INFO
    elif verbose >= 3:
        mob_logger_level = logging.DEBUG
        git_logger_level = logging.DEBUG
        version_checker_thread_logger_level = logging.DEBUG

    bootstrap_cli_app(
        mob_logger_verbosity=mob_logger_level,
        git_logger_verbosity=git_logger_level,
        version_checker_thread_logger_verbosity=version_checker_thread_logger_level,
        check_for_new_version=True,
    )


cli.add_command(start, 'start')
cli.add_command(next, 'next')
cli.add_command(done, 'done')
