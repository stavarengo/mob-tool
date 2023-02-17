import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import pkg_resources
import platformdirs
from dataclasses_json import config, dataclass_json
from injector import inject
from marshmallow import fields

from mobt.Cache import cache_logger
from mobt.Cache.CacheInterface import CacheInterface
from mobt.FileAccess.FileAccess import FileAccess
from mobt.JsonSerializer.JsonSerializerInterface import JsonSerializerInterface


@dataclass_json
@dataclass(frozen=True)
class CacheEntry:
    content: str
    expires_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )

    @property
    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at


_cache_dir = platformdirs.user_cache_dir(
    appname='mob-tool',
    version=pkg_resources.get_distribution('mob-tool').version,
)


@inject
@dataclass(frozen=True)
class FileSystemCache(CacheInterface):
    json: JsonSerializerInterface
    file: FileAccess

    def get(self, cache_id: str) -> Optional[CacheEntry]:
        json_string = self.file.read(self._get_cache_file_path(cache_id))

        if not json_string:
            cache_logger().debug(f'Cache "{cache_id}" not found.')
            return None

        entry = self.json.from_json(CacheEntry, json_string)

        if entry.is_expired:
            cache_logger().debug(f'Cache "{cache_id}" is expired. Deleting it.')
            self.delete(cache_id)
            return None

        cache_logger().debug(f'Cache entry found "{cache_id}". Marked for expire at {entry.expires_at.isoformat()}')

        return entry

    def save(self, cache_id: str, content: str, expires_at: datetime) -> None:
        self.file.save(
            self.json.to_json(CacheEntry(content=content, expires_at=expires_at)),
            self._get_cache_file_path(cache_id)
        )
        cache_logger().debug(f'Saved cache "{cache_id}", to expire at {expires_at.isoformat()}')

    def delete(self, cache_id: str):
        cache_logger().debug(f'Deleted cache "{cache_id}".')

        self.file.delete(self._get_cache_file_path(cache_id))

    def _get_cache_file_path(self, cache_id: str) -> str:
        path = Path(cache_id)
        file_name = path.with_suffix('.json')
        join = os.path.join(_cache_dir, file_name)
        return join
