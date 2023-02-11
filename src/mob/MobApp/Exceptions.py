from mob.GitCli.BranchName import BranchName

from mob.MobException import MobException


class BranchAlreadyExistsAndIsNotMobBranch(MobException):
    @classmethod
    def create(cls, branch_name: BranchName):
        return cls(f"The branch {branch_name} already exists, but it's not a mob branch yet.")


class CurrentBranchIsNotMobBranch(MobException):
    @classmethod
    def create(cls, current_branch: BranchName):
        return cls(f"The current branch {current_branch} is not a mob branch.")


class HeadIsDetached(MobException):
    @classmethod
    def create(cls):
        return cls(f"Head is detached.")
