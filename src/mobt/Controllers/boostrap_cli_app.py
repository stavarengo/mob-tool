import logging
import os
import sys


def _check_for_new_version():
    from mobt import mob_logger
    from mobt.VersionChecker.VersionCheckerService import VersionCheckerService
    from mobt.di import di
    try:
        service = di.get(VersionCheckerService)
        version = service.get_new_version_available()
        if version:
            from mobt import echo
            echo(
                f'Never version available: {version.last_available_version} (installed version: {version.installed_version})',
                fg='bright_yellow')
    except Exception as e:
        mob_logger().debug(f'Failed to check for new version: {e.__class__.__name__} - {str(e)}')


def bootstrap_cli_app(log_level: int, check_for_new_version: bool = True):
    from mobt.Logging.logging_utils import set_log_level
    set_log_level(log_level)

    from mobt.MobApp.GitPopenListener import GitPopenListener
    from mobt.PopenObserver.PopenWrapper import PopenWrapper

    PopenWrapper.add_listener(GitPopenListener())

    if log_level > logging.CRITICAL:
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    if check_for_new_version:
        _check_for_new_version()
