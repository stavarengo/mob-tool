from dataclasses import dataclass

from git import GitCommandError, Repo

from mob.GitCli.BranchName import BranchName
from mob.GitCli.GitPython.GitActions.Exceptions import NonFastForwardPush
from mob.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass(frozen=False)
class _PushUndoContext:
    unset_upstream: bool = False
    delete_remote_branch: bool = False


@dataclass()
class Push(GitAction):
    repo: Repo
    branch_to_push: BranchName
    force: bool = False

    def __post_init__(self):
        self.__context: _PushUndoContext = _PushUndoContext()
        super().__post_init__()

    def _execute(self) -> None:
        branch = self.repo.branches[self.branch_to_push]
        if not branch.tracking_branch():
            self._create_upstream()
            self.__context.unset_upstream = True
            self.__context.delete_remote_branch = True
        else:
            self._push_existing_branch()

    def _undo(self):
        if self.__context.delete_remote_branch:
            self.repo.git.push("origin", "--delete", self.branch_to_push)

        if self.__context.unset_upstream:
            self.repo.git.branch("--unset-upstream", self.branch_to_push)

    def _push_existing_branch(self):
        try:
            if self.force:
                self.repo.git.push("origin", self.branch_to_push, "--force")
            else:
                self.repo.git.push("origin", self.branch_to_push)
        except GitCommandError as e:
            if self._is_non_fast_forward_push(str(e)):
                raise NonFastForwardPush.create()
            raise e

    def _create_upstream(self):
        self.repo.git.push("origin", self.branch_to_push, "--set-upstream")

    @staticmethod
    def _is_non_fast_forward_push(error_message: str):
        return "failed to push some refs" in error_message and "non-fast-forward" in error_message
