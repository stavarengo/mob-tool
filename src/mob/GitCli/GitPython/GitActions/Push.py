from dataclasses import dataclass

from git import Repo

from mob.GitCli.BranchName import BranchName
from mob.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass(frozen=False)
class _PushUndoContext:
    unset_upstream: bool = False
    delete_remote_branch: bool = False
    remote_branch_original_hash: str = None


@dataclass()
class Push(GitAction):
    repo: Repo
    branch_to_push: BranchName

    def __post_init__(self):
        self.__context: _PushUndoContext = _PushUndoContext()
        super().__post_init__()

    def _execute(self) -> None:
        branch = self.repo.branches[self.branch_to_push]
        if not branch.tracking_branch():
            self.repo.git.push("origin", self.branch_to_push, "--set-upstream")
            self.__context.unset_upstream = True
            self.__context.delete_remote_branch = True
        else:
            self.__context.remote_branch_original_hash = branch.tracking_branch().commit.hexsha
            self.repo.git.push("origin", self.branch_to_push)

    def _undo(self):
        if self.__context.delete_remote_branch:
            self.repo.git.push("origin", "--delete", self.branch_to_push)
        elif self.__context.remote_branch_original_hash:
            self.repo.git.push("origin", self.branch_to_push, self.__context.remote_branch_original_hash)

        if self.__context.unset_upstream:
            branch = self.repo.branches[self.branch_to_push]
            self.repo.git.branch("--unset-upstream", branch.name)
