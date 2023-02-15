from dataclasses import dataclass
from typing import Optional

from injector import inject
from packaging.version import Version

from mob.AutoUpdate.AutoUpdateRepository import AutoUpdateRepository
from mob.AutoUpdate.CachedVersion import CacheVersion


@inject
@dataclass
class AutoUpdateService:
    cache: CacheVersion
    repository: AutoUpdateRepository

    def store_available_version(self) -> Optional[Version]:
        return self.is_there_new_version()

    def is_there_new_version(self) -> Optional[Version]:
        available_version = self.cache.get()
        if available_version is None:
            available_version = self.repository.get_available_version()
            if available_version:
                self.cache.save(available_version)

        if available_version and available_version > self.repository.get_current_version():
            return available_version
        return None

    def delete_cache_version(self):
        self.cache.delete()
