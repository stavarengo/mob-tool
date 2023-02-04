from mob.GitCli.BranchName import BranchName

from mob.MobException import MobException


class BranchAlreadyExistsAndIsNotMobBranch(MobException):
    @classmethod
    def create(cls, branch_name: BranchName):
        return cls(f"The branch {branch_name} already exists, but it's not a mob branch yet.")
