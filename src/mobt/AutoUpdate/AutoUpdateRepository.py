from dataclasses import dataclass
from typing import Optional

import pkg_resources
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

    def get_available_version_online(self) -> Optional[Version]:
        return self.package_index_service.get_last_available_version()

    def get_version_installed_locally(self) -> Version:
        if not self.__current_version:
            self.__current_version = Version(pkg_resources.get_distribution('mob-tool').version)
            version_checker_thread_logger().debug(f'Version installed locally: {self.__current_version}')

        return self.__current_version
