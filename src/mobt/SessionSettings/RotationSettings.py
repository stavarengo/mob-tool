from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class RotationSettings:
    driverInMinutes: int = 10
    breakInMinutes: int = 15
    howManyRotationsBeforeBreak: int = 5
    howManyRotationsSinceLastBreak: int = 1
