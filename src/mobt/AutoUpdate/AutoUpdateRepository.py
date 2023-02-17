from dataclasses import dataclass
from importlib.metadata import metadata
from typing import Optional

from injector import inject
from packaging.version import Version

from mobt.AutoUpdate import version_checker_thread_logger
from mobt.AutoUpdate.PyPi import PyPi


@inject
@dataclass
class AutoUpdateRepository:
    package_index_service: PyPi

    def __post_init__(self):
        self.__current_version: Optional[Version] = None

    def get_available_version(self) -> Optional[Version]:
        return self.package_index_service.get_last_available_version()

    def get_current_version(self) -> Version:
        if not self.__current_version:
            setup_metadata = metadata('mob-tool')
            self.__current_version = Version(setup_metadata["version"])
            version_checker_thread_logger().debug(f'Version found in setup metadata: {self.__current_version}')

        return self.__current_version
