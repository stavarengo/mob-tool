from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

from mob.LastTeamMembers.TeamMembers import TeamMembers
from mob.Services.BranchName import BranchName


@dataclass_json
@dataclass(frozen=True)
class MobDataRotation:
    driverInMinutes: int = 10
    breakInMinutes: int = 15
    howManyRotationsBeforeBreak: int = 6


@dataclass_json
@dataclass(frozen=True)
class MobDataSession:
    branch: Optional[BranchName]
    team: TeamMembers
    rotation: MobDataRotation


@dataclass_json
@dataclass(frozen=True)
class MobData:
    session: MobDataSession
    version: str = '0.1.0'

    @staticmethod
    def create(branch: BranchName, team: TeamMembers) -> 'MobData':
        return MobData(MobDataSession(branch, team, MobDataRotation()))

    @staticmethod
    def from_file(path: str) -> 'MobData':
        with open(path) as f:
            return MobData.schema().loads(f.read())

    def save_to_file(self, path: str):
        as_json = self.schema().dumps(self, indent=2)
        with open(path, 'w') as f:
            f.write(as_json)
