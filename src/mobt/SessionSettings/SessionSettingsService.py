import typing
from dataclasses import dataclass, replace

from injector import inject

from mobt.GitCli.GitCliInterface import GitCliInterface
from mobt.LastTeamMembers.TeamMembers import TeamMembers
from mobt.MobSecrets import MobSecrets
from mobt.SessionSettings.Exceptions import SessionSettingsAlreadyExists, SessionSettingsNotFound
from mobt.SessionSettings.RotationSettings import RotationSettings
from mobt.SessionSettings.SessionSettings import SessionSettings
from mobt.SessionSettings.SessionSettingsRepository import SessionSettingsRepository


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

    def update_members(self, new_team: TeamMembers) -> SessionSettings:
        current_settings = self.get()
        old_team = current_settings.team
        if old_team != new_team:
            current_settings = replace(current_settings, team=new_team)
            self.repository.save(current_settings)

        return current_settings

    def delete(self) -> None:
        self.repository.delete()

    def inc_rotation_count(self, inc: int = 1) -> SessionSettings:
        old_session = self.get()
        old_rotation = old_session.rotation
        new_value = old_rotation.howManyRotationsSinceLastBreak + inc
        new_rotation = replace(
            old_rotation,
            howManyRotationsSinceLastBreak=new_value if new_value <= old_rotation.howManyRotationsBeforeBreak else 1
        )
        new_session = replace(old_session, rotation=new_rotation)
        self.repository.save(new_session)

        return new_session
