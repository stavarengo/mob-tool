from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json
from injector import inject
from packaging.version import Version

from mob.DotEnv.DotEnv import DotEnv
from mob.FileAccess.FileAccess import FileAccess
from mob.JsonSerializer.JsonSerializerInterface import JsonSerializerInterface


@dataclass_json
@dataclass
class CacheEntry:
    version: str
    timestamp: float


@inject
@dataclass
class CacheVersion:
    json: JsonSerializerInterface
    file: FileAccess
    dotEnv: DotEnv

    def __post_init__(self):
        self._cache_file_path = None

    def get(self) -> Optional[Version]:
        json_string = self.file.read(self._get_cached_file_path())
        if not json_string:
            return None

        entry = self.json.from_json(CacheEntry, json_string)

        if self._is_cache_expired(entry):
            self.delete()
            return None

        return Version(entry.version)

    def save(self, version: Version) -> None:
        entry = CacheEntry(version=str(version), timestamp=datetime.now().timestamp())
        path = self._get_cached_file_path()
        content = self.json.to_json(entry)
        self.file.save(content, path)

    def delete(self):
        self.file.delete(self._get_cached_file_path())

    def _is_cache_expired(self, entry: CacheEntry) -> bool:
        return (datetime.now().timestamp() - entry.timestamp) > 60 * 60 * 12

    def _get_cached_file_path(self) -> str:
        if not self._cache_file_path:
            self._cache_file_path = '/tmp/.mob.version_cache'

        return self._cache_file_path
