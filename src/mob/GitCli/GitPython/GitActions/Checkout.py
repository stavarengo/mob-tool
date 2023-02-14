import typing
from dataclasses import dataclass

from git import Repo

from mob.GitCli.BranchName import BranchName
from mob.GitCli.Exceptions import WorkingDirectoryNotClean
from mob.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass()
class Checkout(GitAction):
    repo: Repo
    branch_name: BranchName
    original_head_ref: typing.Optional[str] = None
    fail_if_dirty: bool = True

    def _execute(self) -> None:
        if self.fail_if_dirty:
            self.__fail_if_dirty()

        self.original_head_ref = BranchName(
            self.original_head_ref or self.repo.active_branch.name or self.repo.active_branch.commit.hexsha
        )

        if self.original_head_ref == self.branch_name:
            return

        self.repo.git.checkout(self.branch_name)

    def _undo(self):
        if self.original_head_ref == self.branch_name:
            return
        self.repo.git.checkout(self.original_head_ref)

    def __fail_if_dirty(self):
        if self.repo.is_dirty():
            raise WorkingDirectoryNotClean.create()
