from dataclasses import dataclass

from injector import inject

from mob.LastTeamMembers.TeamMembers import TeamMembers
from mob.MobSecrets import MobSecrets


@inject
@dataclass
class LastTeamMembersRepository:
    secrets: MobSecrets

    def load_team(self) -> TeamMembers | None:
        try:
            with open(self.secrets.last_team_members_file_path(), 'r') as f:
                file_contents = f.read()
                if file_contents == '':
                    return None
                return TeamMembers.schema().loads(file_contents)
        except FileNotFoundError:
            return None

    def save_team(self, members: TeamMembers):
        with open(self.secrets.last_team_members_file_path(), 'w') as f:
            f.write(TeamMembers.schema().dumps(members, indent=2))
