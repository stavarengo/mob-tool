import typing
from dataclasses import dataclass

from injector import inject

from mob.GitCli.GitCliInterface import GitCliInterface
from mob.LastTeamMembers.LastTeamMembersRepository import LastTeamMembersRepository
from mob.LastTeamMembers.TeamMembers import TeamMembers
from mob.MobSecrets import MobSecrets


@inject
@dataclass
class LastTeamMembersService:
    repository: LastTeamMembersRepository
    git: GitCliInterface
    secrets: MobSecrets

    def get_last_team(self) -> typing.Optional[TeamMembers]:
        return self.repository.load_team()

    def save_last_team(self, members: TeamMembers):
        self.repository.save_team(members)
        self.git.add_to_git_info_exclude(self.secrets.last_team_members_file_path())
