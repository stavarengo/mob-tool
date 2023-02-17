from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import config, dataclass_json
from marshmallow import fields


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


@dataclass(frozen=True)
class CacheInterface(ABC):

    @abstractmethod
    def get(self, cache_id: str) -> Optional[CacheEntry]:
        pass

    @abstractmethod
    def save(self, cache_id: str, content: str, expires_at: datetime) -> None:
        pass

    @abstractmethod
    def delete(self, cache_id: str):
        pass

    @abstractmethod
    def _get_cache_file_path(self, cache_id: str) -> str:
        pass
