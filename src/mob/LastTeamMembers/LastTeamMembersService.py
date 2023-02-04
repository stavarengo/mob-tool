import json
from dataclasses import dataclass

from injector import inject

from mob.LastTeamMembers.LastTeamMembersRepository import LastTeamMembersRepository
from mob.LastTeamMembers.TeamMembers import TeamMembers


@inject
@dataclass
class LastTeamMembersService:
    repository: LastTeamMembersRepository

    def get_last_team(self) -> TeamMembers:
        return self.repository.load_team()

    def save_last_team(self, members: TeamMembers):
        self.__validate_team(members)
        with open(self.repository.filename, 'w') as f:
            f.write(json.dumps(members.__dict__))

    @staticmethod
    def __validate_team(members: TeamMembers | None) -> None:
        if not members or members.len < 3:
            raise ValueError('You must provide at least three members.')
