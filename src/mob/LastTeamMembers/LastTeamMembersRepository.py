from dataclasses import dataclass

from injector import inject

from mob.LastTeamMembers.TeamMembers import TeamMembers
from mob.MobSecrets import MobSecrets


@inject
@dataclass
class LastTeamMembersRepository:
    mob: MobSecrets

    def load_team(self) -> TeamMembers | None:
        try:
            with open(self.mob.last_team_members_file_path(), 'r') as f:
                return TeamMembers.schema.loads(f.read())
        except FileNotFoundError:
            return None
