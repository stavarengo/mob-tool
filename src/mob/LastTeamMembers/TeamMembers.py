import random
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from mob.LastTeamMembers.Exceptions import ThereAreDuplicatedTeamMembers, YouCantMobWithLessThanTwoMembers
from mob.LastTeamMembers.TeamMemberName import TeamMemberName


@dataclass_json
@dataclass(frozen=True)
class TeamMembers:
    team: list[TeamMemberName]

    def __post_init__(self):
        unique_team = list(dict.fromkeys(self.team))
        if len(self.team) != len(unique_team):
            raise ThereAreDuplicatedTeamMembers.create()

        if self.len < 2:
            raise YouCantMobWithLessThanTwoMembers.create()

    @property
    def driver(self) -> TeamMemberName:
        return self.team[0]

    @property
    def navigator(self) -> TeamMemberName:
        return self.team[1]

    @property
    def len(self) -> int:
        return len(self.team)

    def randomize(self) -> 'TeamMembers':
        print(f'randomize[{self.len}]: {self}')
        if self.len == 2:
            new = TeamMembers([self.navigator, self.driver])
        else:
            new_team = self.team.copy()
            random.shuffle(new_team)
            new = TeamMembers(new_team)

        if new == self:
            return self.randomize()
        return new

    def __str__(self) -> str:
        return ', '.join(self.team)
