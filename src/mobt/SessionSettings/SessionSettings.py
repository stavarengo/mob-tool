from dataclasses import dataclass

from dataclasses_json import dataclass_json

from mobt.LastTeamMembers.TeamMembers import TeamMembers
from mobt.SessionSettings.RotationSettings import RotationSettings


@dataclass_json
@dataclass(frozen=True)
class SessionSettings:
    team: TeamMembers
    rotation: RotationSettings
    version: str = '0.1.0'
