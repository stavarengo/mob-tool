import git


class MobProgramming:
    def __init__(self):
        # Initializing the repository
        self.repo = git.Repo()
        self.team_members = team_members
        self.mobbing_session = None

    def start_session(self):
        if self.mobbing_session:
            print("A mobbing session is already in progress.")
            return

        self.mobbing_session = True
        print("Mobbing session started with team members:")
        for member in self.team_members:
            print(member)

    def end_session(self):
        if not self.mobbing_session:
            print("No mobbing session in progress.")
            return

        self.mobbing_session = None
        print("Mobbing session ended.")

    def add_team_member(self, member: str):
        self.team_members.append(member)
        print(f"{member} has been added to the team.")

    def remove_team_member(self, member: str):
        self.team_members.remove(member)
        print(f"{member} has been removed from the team.")
