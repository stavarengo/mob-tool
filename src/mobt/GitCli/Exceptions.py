from mobt.GitCli.BranchName import BranchName
from mobt.MobException import MobException


class WorkingDirectoryNotClean(MobException):
    @classmethod
    def create(cls):
        return cls("Work directory is not clean.")

    def extra_help(self) -> str:
        return "Please clean your work directory before trying again."


class ThereIsNoDifferenceBetweenTheCurrentBranchAndTheMainBranch(MobException):

    @classmethod
    def create(cls, current_branch_name: str, main_branch_name: str):
        return cls(
            f"There is no difference between branches '{current_branch_name}' and '{main_branch_name}'."
        )

    def extra_help(self) -> str:
        return "That means there is nothing to be merged back to the main branch."


class CanNotFindMainBranch(MobException):
    @classmethod
    def create(cls, all_possible_names: list[BranchName]) -> 'CanNotFindMainBranch':
        return cls(f"Can not find main branch. All possible names: {all_possible_names}.")
