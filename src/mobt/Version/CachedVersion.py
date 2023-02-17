from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from dataclasses_json import config, dataclass_json
from injector import inject
from marshmallow import fields
from packaging.version import Version

from mobt.FileAccess.FileAccess import FileAccess
from mobt.JsonSerializer.JsonSerializerInterface import JsonSerializerInterface
from mobt.Version import version_checker_thread_logger


@dataclass_json
@dataclass
class CacheEntry:
    version: str
    expires_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )


@inject
@dataclass
class CacheVersion:
    json: JsonSerializerInterface
    file: FileAccess

    def __post_init__(self):
        self._cache_file_path = None

    def get(self) -> Optional[Version]:
        json_string = self.file.read(self._get_cached_file_path())
        if not json_string:
            version_checker_thread_logger().debug(f'Available version number not cached')
            return None

        entry = self.json.from_json(CacheEntry, json_string)

        if self._is_cache_expired(entry):
            version_checker_thread_logger().debug(f'Available version number cache is expired. Deleting cache.')

            self.delete()
            return None

        version_checker_thread_logger().debug(
            f'Available version number returned from cache: {entry.version}. Cache expires in {entry.expires_at.isoformat()}')

        return Version(entry.version)

    def save(self, version: Version) -> None:
        expires_at = datetime.now() + timedelta(hours=12)
        entry = CacheEntry(version=str(version), expires_at=expires_at)
        path = self._get_cached_file_path()
        content = self.json.to_json(entry)

        version_checker_thread_logger().debug(f'Available version number saved in cache: {content}')

        self.file.save(content, path)

    def delete(self):
        version_checker_thread_logger().debug(f'Available version number cache deleted.')
        self.file.delete(self._get_cached_file_path())

    def _is_cache_expired(self, entry: CacheEntry) -> bool:
        return datetime.now() > entry.expires_at

    def _get_cached_file_path(self) -> str:
        if not self._cache_file_path:
            self._cache_file_path = '/tmp/.mobt.version_cache'

        return self._cache_file_path
