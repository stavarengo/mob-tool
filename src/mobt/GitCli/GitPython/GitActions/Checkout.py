import typing
from dataclasses import dataclass

from git import Repo

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction
from mobt.GitCli.GitPython.GitActions.GitActionWasExecuted import GitActionWasExecuted


@dataclass()
class Checkout(GitAction):
    repo: Repo
    branch_name: BranchName
    event_manager: EventManager
    original_head_ref: typing.Optional[str] = None
    fail_if_dirty: bool = True

    def __post_init__(self):
        super().__post_init__()
        self._delete_local_branch = False

    def _execute(self) -> None:
        self.original_head_ref = BranchName(
            self.original_head_ref or self.repo.active_branch.name or self.repo.active_branch.commit.hexsha
        )

        if self.original_head_ref == self.branch_name:
            return

        self._delete_local_branch = not str(self.branch_name) in self.repo.branches

        human_log = f'Checking out branch "{self.branch_name}"'

        self.event_manager.dispatch_event(GitActionWasExecuted(self.__class__, human_log=f'{human_log}'))

        self.repo.git.checkout(self.branch_name)

    def _undo(self):
        if self.original_head_ref != self.branch_name:
            self.repo.git.checkout(self.original_head_ref)

        if self._delete_local_branch:
            self.repo.git.branch('-D', self.branch_name)
