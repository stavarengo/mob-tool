from dataclasses import dataclass


@dataclass
class TeamMembersService:
    def __init__(self):
        self.team_members = []

    def add_team_member(self, team_member):
        self.team_members.append(team_member)

    def get_team_members(self):
        return self.team_members

    def remove_team_member(self, team_member):
        self.team_members.remove(team_member)

    def clear_team_members(self):
        self.team_members.clear()

    def next_driver(self):
        return len(self.team_members)

    def get_team_member(self, index):
        return self.team_members[index]

    def get_team_member_index(self, team_member):
        return self.team_members.index(team_member)

    def is_team_member(self, team_member):
        return team_member in self.team_members

    def get_team_members_string(self):
        return ', '.join(self.team_members)

    def get_team_members_string_with_index(self):
        return ', '.join([f'{index + 1}: {team_member}' for index, team_member in enumerate(self.team_members)])
