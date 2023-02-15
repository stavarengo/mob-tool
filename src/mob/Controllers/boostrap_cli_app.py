import logging

import click

from mob.AutoUpdate.AutoUpdateService import AutoUpdateService
from mob.AutoUpdate.VersionCheckerThread import version_checker_thread_logger
from mob.GitCli.GitPython import git_logger
from mob.Logging import mob_logger
from mob.di import di


def _set_verbosity(verbose: bool):
    if verbose:
        mob_logger().setLevel(logging.DEBUG)
        git_logger().setLevel(logging.DEBUG)
        version_checker_thread_logger().setLevel(logging.DEBUG)


def bootstrap_cli_app(verbose: bool, check_for_new_version: bool = True):
    _set_verbosity(verbose)
    if check_for_new_version:
        try:
            service = di.get(AutoUpdateService)
            version = service.is_there_new_version()
            if version:
                print(click.style(f'New version available: {version}', fg='bright_yellow'))
        except Exception as e:
            mob_logger().debug(f'Failed to check for new version: {e.__class__.__name__} - {str(e)}')
