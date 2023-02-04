from mob.LastTeamMembers.Exceptions import MemberNameCanNotBeEmpty


class TeamMemberName(str):
    def __init__(self, value: str):
        value = value.strip()
        if not value:
            raise MemberNameCanNotBeEmpty.create()
        self = value
