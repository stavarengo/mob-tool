import logging
import sys
import threading

from injector import inject

from mob.AutoUpdate.AutoUpdateService import AutoUpdateService
from mob.DotEnv.DotEnv import DotEnv
from mob.di import di


def version_checker_thread_logger() -> logging.Logger:
    return logging.getLogger('mob.AutoUpdate.VersionCheckerThread')


if di.get(DotEnv).is_development():
    version_checker_thread_logger().addHandler(logging.StreamHandler(sys.stdout))
    version_checker_thread_logger().setLevel(logging.DEBUG)


@inject
class VersionCheckerThread(threading.Thread):

    def __init__(self, service: AutoUpdateService):
        super().__init__()
        self._service = service
        self._callback = None
        version_checker_thread_logger().debug("Thread created")

    def run(self):
        version_checker_thread_logger().debug("Thread started")
        try:
            self._run()
            version_checker_thread_logger().debug('Thread finished')
        except Exception as e:
            version_checker_thread_logger().debug(f'Thread exception: {e.__class__.__name__} - {str(e)}')

    def _run(self):
        if not self.callback:
            raise Exception("Callback is not set")
        try:
            version = self._service.is_there_new_version()
            version_checker_thread_logger().debug(f'Calling callback with version: {version}')
            self.callback(version)
        except Exception as e:
            version_checker_thread_logger().debug(f'Thread ignored exception: {e.__class__.__name__} - {str(e)}')

    @property
    def callback(self) -> callable:
        return self._callback

    @callback.setter
    def callback(self, value: callback):
        self._callback = value
