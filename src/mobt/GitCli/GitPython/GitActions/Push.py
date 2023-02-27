from dataclasses import dataclass

from git import GitCommandError, Repo

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.GitPython.GitActions.Exceptions import NonFastForwardPush
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction
from mobt.GitCli.GitPython.GitActions.GitActionWasExecuted import GitActionWasExecuted


@dataclass(frozen=False)
class _PullRequestData:
    term: str
    create_url: str
    view_url: str
    event_manager: EventManager

    def __str__(self):
        return f'Create new {self.term}: {self.create_url}'


@dataclass(frozen=False)
class _PushUndoContext:
    unset_upstream: bool = False
    delete_remote_branch: bool = False
    remote_original_commit: str = None


@dataclass()
class Push(GitAction):
    repo: Repo
    branch_to_push: BranchName
    event_manager: EventManager
    force: bool = False

    def __post_init__(self):
        self.__context: _PushUndoContext = _PushUndoContext()
        super().__post_init__()

    def _execute(self) -> None:
        branch = self.repo.branches[self.branch_to_push]

        self.event_manager.dispatch_event(
            GitActionWasExecuted(
                self.__class__,
                f'Pushing "{self.branch_to_push}" to "origin/{self.branch_to_push}"'
            )
        )

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

        if self.__context.remote_original_commit:
            branch = self.repo.branches[self.branch_to_push]
            tracking_branch = branch.tracking_branch()
            if not self._is_branch_in_sync_with(tracking_branch, self.__context.remote_original_commit):
                self.repo.git.push(
                    '--force',
                    'origin',
                    f'{self.__context.remote_original_commit}:{self.branch_to_push}'
                )

    def _push_existing_branch(self):
        branch = self.repo.branches[self.branch_to_push]
        tracking_branch = branch.tracking_branch()

        if self._is_branch_in_sync_with(tracking_branch, branch.commit.hexsha):
            return

        self.__context.remote_original_commit = tracking_branch.commit.hexsha

        try:
            if self.force:
                self.repo.git.push("origin", self.branch_to_push, "--force")
            else:
                self.repo.git.push("origin", self.branch_to_push)
        except GitCommandError as e:
            if self._is_non_fast_forward_push(str(e)):
                raise NonFastForwardPush.create()
            raise e

    def _is_branch_in_sync_with(self, branch, at_commit) -> bool:
        try:
            if branch and branch.commit.hexsha == at_commit:
                # Local and remote are in sync
                return True
        except ValueError as e:
            e_str = str(e)
            if 'Reference at' not in e_str and 'does not exist' not in e_str:
                raise e

        return False

    def _create_upstream(self):
        self.repo.git.push("origin", self.branch_to_push, "--set-upstream")

    @staticmethod
    def _is_non_fast_forward_push(error_message: str):
        return "failed to push some refs" in error_message and "non-fast-forward" in error_message
