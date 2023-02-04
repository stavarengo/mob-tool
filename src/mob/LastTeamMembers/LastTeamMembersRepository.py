from dataclasses import dataclass

from injector import inject

from mob.FileAccess.FileAccess import FileAccess
from mob.LastTeamMembers.TeamMembers import TeamMembers
from mob.MobSecrets import MobSecrets


@inject
@dataclass
class LastTeamMembersRepository:
    secrets: MobSecrets
    file: FileAccess

    def load_team(self) -> TeamMembers | None:
        contents = self.file.read(self.secrets.last_team_members_file_path())
        return contents and TeamMembers.schema().loads(contents) or None

    def save_team(self, members: TeamMembers):
        self.file.save(TeamMembers.schema().dumps(members, indent=2), self.secrets.last_team_members_file_path())
