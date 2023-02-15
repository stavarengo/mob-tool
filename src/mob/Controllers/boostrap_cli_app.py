import click

from mob.AutoUpdate.AutoUpdateService import AutoUpdateService
from mob.AutoUpdate.VersionCheckerThread import version_checker_thread_logger
from mob.GitCli.GitPython import git_logger
from mob.Logging import mob_logger
from mob.di import di


def _set_verbosity(mob_logger_level: int, git_logger_level: int, version_checker_thread_logger_level: int) -> None:
    mob_logger().setLevel(mob_logger_level)
    git_logger().setLevel(git_logger_level)
    version_checker_thread_logger().setLevel(version_checker_thread_logger_level)


def _check_for_new_version():
    try:
        service = di.get(AutoUpdateService)
        version = service.is_there_new_version()
        if version:
            mob_logger().warning(click.style(f'New version available: {version}', fg='bright_yellow'))
    except Exception as e:
        version_checker_thread_logger().debug(f'Failed to check for new version: {e.__class__.__name__} - {str(e)}')


def bootstrap_cli_app(mob_logger_verbosity: int, git_logger_verbosity: int,
                      version_checker_thread_logger_verbosity: int,
                      check_for_new_version: bool = True):
    _set_verbosity(
        mob_logger_level=mob_logger_verbosity,
        git_logger_level=git_logger_verbosity,
        version_checker_thread_logger_level=version_checker_thread_logger_verbosity,
    )
    if check_for_new_version:
        _check_for_new_version()
