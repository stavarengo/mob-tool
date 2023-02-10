from dataclasses_json import dataclass_json

from mob.LastTeamMembers.Exceptions import MemberNameCanNotBeEmpty


@dataclass_json
class TeamMemberName(str):
    def __init__(self, value: str):
        value = value.strip()
        if not value:
            raise MemberNameCanNotBeEmpty.create()
        self = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"
