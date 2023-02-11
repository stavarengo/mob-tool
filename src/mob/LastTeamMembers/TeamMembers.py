import random
from dataclasses import dataclass, field

from dataclasses_json import config, dataclass_json
from marshmallow import fields

from mob.LastTeamMembers.Exceptions import ThereAreDuplicatedTeamMembers, YouCantMobWithLessThanTwoMembers
from mob.LastTeamMembers.TeamMemberName import TeamMemberName


@dataclass_json
@dataclass(frozen=True)
class TeamMembers:
    members: list[TeamMemberName] = field(
        metadata=config(
            decoder=lambda value: [TeamMemberName(n) for n in value],
            mm_field=fields.List(fields.Str)
        )
    )

    def __post_init__(self):
        unique_team = list(dict.fromkeys(self.members))
        if len(self.members) != len(unique_team):
            raise ThereAreDuplicatedTeamMembers.create()

        if self.len < 2:
            raise YouCantMobWithLessThanTwoMembers.create()

    @property
    def driver(self) -> TeamMemberName:
        return self.members[0]

    @property
    def navigator(self) -> TeamMemberName:
        return self.members[1]

    @property
    def next_navigator(self) -> TeamMemberName:
        return self.members[2]

    @property
    def len(self) -> int:
        return len(self.members)

    def rotate(self) -> 'TeamMembers':
        return TeamMembers([self.navigator, self.next_navigator, *self.members[3:], self.driver])

    def randomize(self) -> 'TeamMembers':
        if self.len == 2:
            new = TeamMembers([self.navigator, self.driver])
        else:
            new_team = self.members.copy()
            random.shuffle(new_team)
            new = TeamMembers(new_team)

        if new == self:
            return self.randomize()
        return new

    def __str__(self) -> str:
        return ', '.join(self.members)
