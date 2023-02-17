from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from injector import inject
from packaging.version import Version


@inject
@dataclass(frozen=True)
class SupplierInterface(ABC):
    @abstractmethod
    def get_version(self) -> Optional[Version]:
        pass
