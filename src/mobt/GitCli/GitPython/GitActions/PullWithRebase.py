import os
from dataclasses import dataclass

from git import Repo

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.GitPython import log_undoing_all_git_commands
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction
from mobt.GitCli.GitPython.GitActions.GitActionWasExecuted import GitActionWasExecuted


@dataclass()
class PullWithRebase(GitAction):
    repo: Repo
    event_manager: EventManager

    def __post_init__(self):
        super().__post_init__()
        self._original_sha = None

    def _execute(self) -> None:
        tracking_branch = self.repo.active_branch.tracking_branch()
        if not tracking_branch:
            return

        try:
            remote_sha = tracking_branch.commit.hexsha
        except ValueError as e:
            e_str = str(e)
            if 'Reference at' in e_str and 'does not exist' in e_str:
                return
            raise e

        self._original_sha = self.repo.active_branch.commit.hexsha

        if self._original_sha == remote_sha:
            return

        try:
            self.event_manager.dispatch_event(
                GitActionWasExecuted(
                    self.__class__,
                    f'Rebasing local "{self.repo.active_branch}" on top of "{tracking_branch.name}"'
                )
            )
            self.repo.git.pull('--rebase')
        except Exception as e:
            log_undoing_all_git_commands()
            self._undo()
            raise e

    def _undo(self):
        if not self._original_sha:
            return

        git_dir = self.repo.git_dir
        rebase_merge_exists = os.path.exists(os.path.join(git_dir, 'rebase-merge'))
        if rebase_merge_exists or os.path.exists(os.path.join(git_dir, 'rebase-apply')):
            self.repo.git.rebase('--abort')

        if self._original_sha == self.repo.active_branch.commit.hexsha:
            return

        self.repo.git.reset("--hard", self._original_sha)
