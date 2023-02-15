from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class RotationSettings:
    driverInMinutes: float = 10
    breakInMinutes: float = 15
    howManyRotationsBeforeBreak: int = 6
