import os
from dataclasses import dataclass

from git import Repo

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.GitPython import log_undoing_all_git_commands
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction
from mobt.GitCli.GitPython.GitActions.GitActionWasExecuted import GitActionWasExecuted


@dataclass()
class Rebase(GitAction):
    repo: Repo
    rebase_onto: BranchName
    event_manager: EventManager
    log_undoing_git_commands_title: bool = True

    def __post_init__(self):
        super().__post_init__()
        self._original_sha = None

    def _execute(self) -> None:
        self._original_sha = self.repo.active_branch.commit.hexsha

        if self._original_sha == self.repo.references[self.rebase_onto].commit:
            return

        self.event_manager.dispatch_event(
            GitActionWasExecuted(
                self.__class__,
                f'Rebasing "{self.repo.active_branch}" onto "{self.rebase_onto}"'
            )
        )

        try:
            self.repo.git.rebase(self.rebase_onto)
        except Exception as e:
            if self.log_undoing_git_commands_title:
                log_undoing_all_git_commands()
            self._undo()
            raise e

    def _undo(self):
        git_dir = self.repo.git_dir
        rebase_merge_exists = os.path.exists(os.path.join(git_dir, 'rebase-merge'))
        if rebase_merge_exists or os.path.exists(os.path.join(git_dir, 'rebase-apply')):
            self.repo.git.rebase('--abort')

        if not self._original_sha or self._original_sha == self.repo.active_branch.commit.hexsha:
            return

        self.repo.git.reset("--hard", self._original_sha)
