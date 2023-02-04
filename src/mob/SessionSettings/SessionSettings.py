from dataclasses import dataclass

from dataclasses_json import dataclass_json

from mob.LastTeamMembers.TeamMembers import TeamMembers
from mob.SessionSettings.RotationSettings import RotationSettings


@dataclass_json
@dataclass(frozen=True)
class SessionSettings:
    team: TeamMembers
    rotation: RotationSettings
    version: str = '0.1.0'
