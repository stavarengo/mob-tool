from dataclasses import dataclass
from typing import Optional

from injector import inject
from packaging.version import Version

from mobt.Version.CachedVersion import CacheVersion
from mobt.Version.VersionRepository import VersionRepository


@inject
@dataclass
class VersionService:
    cache: CacheVersion
    repository: VersionRepository

    def get_current_installed_version(self) -> Version:
        return self.repository.get_version_installed_locally()

    def store_available_version(self) -> Optional[Version]:
        return self.is_there_new_version()

    def is_there_new_version(self) -> Optional[Version]:
        available_version = self.cache.get()
        if available_version is None:
            available_version = self.repository.get_available_version_online()
            if available_version:
                self.cache.save(available_version)

        if available_version and available_version > self.repository.get_version_installed_locally():
            return available_version
        return None

    def delete_cache_version(self):
        self.cache.delete()
