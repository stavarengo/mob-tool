import typing
from dataclasses import dataclass

from git import Repo

from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.Exceptions import WorkingDirectoryNotClean
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass()
class Reset(GitAction):
    repo: Repo
    reset_to: BranchName
    hard: bool

    def __post_init__(self):
        self.__original_head_ref: typing.Optional[str] = None
        super().__post_init__()

    def _execute(self) -> None:
        self.__fail_if_dirty()

        self.__original_head_ref = BranchName(self.repo.active_branch.commit.hexsha)

        if self.__original_head_ref == self.reset_to:
            return

        self._reset(self.reset_to, self.hard)

    def _reset(self, reset_to: str, hard: bool = False) -> None:
        self.repo.git.reset("--hard" if hard else "--soft", reset_to)

    def _undo(self):
        if self.__original_head_ref == self.reset_to:
            return
        self._reset(self.__original_head_ref, hard=True)

    def __fail_if_dirty(self):
        if self.repo.is_dirty(untracked_files=True):
            raise WorkingDirectoryNotClean.create()
