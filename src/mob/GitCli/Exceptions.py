from mob.GitCli.BranchName import BranchName
from mob.MobException import MobException


class WorkingDirectoryNotClean(MobException):
    @classmethod
    def create(cls):
        return cls("Work directory is not clean.")


class ThereIsNoDifferenceBetweenTheCurrentBranchAndTheMainBranch(MobException):
    @classmethod
    def create(cls, current_branch_name: str, main_branch_name: str):
        return cls(
            f"There is no difference between the current branch '{current_branch_name}' and the main branch '{main_branch_name}'.")


class CanNotFindMainBranch(MobException):
    @classmethod
    def create(cls, all_possible_names: list[BranchName]) -> 'CanNotFindMainBranch':
        return cls(f"Can not find main branch. All possible names: {all_possible_names}.")
