import typing
from dataclasses import dataclass

from injector import inject

from mobt.FileAccess.FileAccess import FileAccess
from mobt.JsonSerializer.JsonSerializerInterface import JsonSerializerInterface
from mobt.LastTeamMembers.TeamMembers import TeamMembers
from mobt.MobSecrets import MobSecrets


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
