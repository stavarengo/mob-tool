import typing
from dataclasses import dataclass, replace

from injector import inject

from mob.GitCli.GitCliInterface import GitCliInterface
from mob.LastTeamMembers.TeamMembers import TeamMembers
from mob.MobSecrets import MobSecrets
from mob.SessionSettings.Exceptions import SessionSettingsAlreadyExists, SessionSettingsNotFound
from mob.SessionSettings.RotationSettings import RotationSettings
from mob.SessionSettings.SessionSettings import SessionSettings
from mob.SessionSettings.SessionSettingsRepository import SessionSettingsRepository


@inject
@dataclass
class SessionSettingsService:
    repository: SessionSettingsRepository
    git: GitCliInterface
    secrets: MobSecrets

    def find(self) -> typing.Optional[SessionSettings]:
        return self.repository.find()

    def get(self) -> SessionSettings:
        session_settings = self.find()
        if not session_settings:
            raise SessionSettingsNotFound.create()
        return session_settings

    def create(self, members: TeamMembers, rotation: RotationSettings) -> SessionSettings:
        if self.repository.find():
            raise SessionSettingsAlreadyExists.create()
        data = SessionSettings(members, rotation)
        self.repository.save(data)
        return data

    def update_members(self, team: TeamMembers) -> SessionSettings:
        new_session = replace(self.get(), team=team)

        self.repository.save(new_session)
        return new_session

    def delete(self) -> None:
        self.repository.delete()
