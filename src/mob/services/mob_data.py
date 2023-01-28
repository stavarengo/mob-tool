from dataclasses import dataclass
from typing import Optional, Tuple

from dataclasses_json import dataclass_json


@dataclass(frozen=True)
class MobDataRotation:
    driverInMinutes: int = 10
    breakInMinutes: int = 15
    howManyRotationsBeforeBreak: int = 6


@dataclass(frozen=True)
class MobDataTeam:
    driver: str
    navigator: str
    restOfTheTeam: Tuple[str, ...]


@dataclass(frozen=True)
class MobDataSession:
    branch: Optional[str]
    team: MobDataTeam
    rotation: MobDataRotation


@dataclass_json
@dataclass(frozen=True)
class MobData:
    session: MobDataSession
    version: str = '0.1.0'
