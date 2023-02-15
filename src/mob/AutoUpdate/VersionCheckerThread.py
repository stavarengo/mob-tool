import logging
import sys
import threading

from injector import inject

from mob.AutoUpdate.AutoUpdatedService import AutoUpdateService
from mob.DotEnv.DotEnv import DotEnv
from mob.di import di

thread_logger = logging.getLogger('mob.AutoUpdate.VersionCheckerThread')
if di.get(DotEnv).is_development():
    thread_logger.addHandler(logging.StreamHandler(sys.stdout))
    thread_logger.level = logging.DEBUG


@inject
class VersionCheckerThread(threading.Thread):

    def __init__(self, service: AutoUpdateService):
        super().__init__()
        self._service = service
        self._callback = None
        thread_logger.debug("Thread created")

    def run(self):
        thread_logger.debug("Thread started")
        try:
            self._run()
            thread_logger.debug('Thread finished')
        except Exception as e:
            thread_logger.debug(f'Thread exception: {e.__class__.__name__} - {str(e)}')

    def _run(self):
        if not self.callback:
            raise Exception("Callback is not set")
        try:
            version = self._service.is_there_new_version()
            thread_logger.debug(f'Calling callback with version: {version}')
            self.callback(version)
        except Exception as e:
            thread_logger.debug(f'Thread ignored exception: {e.__class__.__name__} - {str(e)}')

    @property
    def callback(self) -> callable:
        return self._callback

    @callback.setter
    def callback(self, value: callback):
        self._callback = value
