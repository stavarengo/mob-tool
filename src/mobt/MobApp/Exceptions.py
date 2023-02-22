from mobt.GitCli.BranchName import BranchName

from mobt.MobException import MobException


class BranchAlreadyExistsAndIsNotMobBranch(MobException):
    @classmethod
    def create(cls, branch_name: BranchName):
        return cls(f"The branch {branch_name} already exists, but it's not a mob branch yet.")

    def extra_help(self) -> str:
        return "Use the option `-f` if you really want to start a mob session on this branch."


class BranchIsAlreadyAnMobBranch(MobException):
    @classmethod
    def create(cls, branch_name: BranchName):
        return cls(f"The branch {branch_name} is already a mob branch.")


class CurrentBranchIsNotMobBranch(MobException):
    @classmethod
    def create(cls, current_branch: BranchName):
        return cls(f"The current branch {current_branch} is not a mob branch.")


class BranchNotFound(MobException):
    @classmethod
    def create(cls, branch: BranchName):
        return cls(f"Branch {branch} not found.")


class HeadIsDetached(MobException):
    @classmethod
    def create(cls):
        return cls(f"Head is detached.")
