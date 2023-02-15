from dataclasses import dataclass
from importlib.metadata import metadata
from typing import Optional

from injector import inject
from packaging.version import Version

from mob.AutoUpdate.PyPi import PyPi
from mob.DotEnv.DotEnv import DotEnv


@inject
@dataclass
class AutoUpdateRepository:
    package_index_service: PyPi
    dotEnv: DotEnv

    def __post_init__(self):
        self.__current_version: Optional[Version] = None

    def get_available_version(self) -> Optional[Version]:
        return self.package_index_service.get_last_available_version()

    def get_current_version(self) -> Version:
        if not self.__current_version:
            setup_metadata = metadata(self.dotEnv.PYPI_APP_NAME)
            self.__current_version = Version(setup_metadata["version"])

        return self.__current_version
