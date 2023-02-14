import typing
from dataclasses import dataclass

from injector import inject

from mob.FileAccess.FileAccess import FileAccess
from mob.JsonSerializer.JsonSerializerInterface import JsonSerializerInterface
from mob.LastTeamMembers.TeamMembers import TeamMembers
from mob.MobSecrets import MobSecrets


@inject
@dataclass
class LastTeamMembersRepository:
    secrets: MobSecrets
    file: FileAccess
    serializer: JsonSerializerInterface

    def load_team(self) -> typing.Optional[TeamMembers]:
        contents = self.file.read(self.secrets.last_team_members_file_path())
        return contents and self.serializer.from_json(TeamMembers, contents) or None

    def save_team(self, members: TeamMembers):
        self.file.save(self.serializer.to_json(members), self.secrets.last_team_members_file_path())
