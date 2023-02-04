from mob.GitCli.BranchName import BranchName

from mob.MobException import MobException


class NotMobBranch(MobException):
    pass

    @classmethod
    def create(cls, branch_name: BranchName):
        return cls(f'Branch "{branch_name}" is not a mob branch.')


class WorkingDirectoryNotClean(MobException):
    @classmethod
    def create(cls):
        return cls("Work directory is not clean.")
