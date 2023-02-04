from dataclasses import dataclass

from injector import inject

from mob.GitCli.GitCliInterface import GitCliInterface
from mob.LastTeamMembers.TeamMembers import TeamMembers
from mob.MobSecrets import MobSecrets
from mob.SessionSettings.Exceptions import SessionSettingsAlreadyExists
from mob.SessionSettings.RotationSettings import RotationSettings
from mob.SessionSettings.SessionSettings import SessionSettings
from mob.SessionSettings.SessionSettingsRepository import SessionSettingsRepository


@inject
@dataclass
class SessionSettingsService:
    repository: SessionSettingsRepository
    git: GitCliInterface
    secrets: MobSecrets

    def create(self, members: TeamMembers, rotation: RotationSettings) -> SessionSettings:
        if self.repository.find() is not None:
            raise SessionSettingsAlreadyExists.create()
        data = SessionSettings(members, rotation)
        self.repository.save(data)
        return data
