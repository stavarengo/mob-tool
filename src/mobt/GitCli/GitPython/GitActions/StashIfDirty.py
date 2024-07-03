import datetime
from dataclasses import dataclass

from git import Repo

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction
from mobt.GitCli.GitPython.GitActions.GitActionWasExecuted import GitActionWasExecuted


@dataclass()
class StashIfDirty(GitAction):
    repo: Repo
    stash_name: str
    event_manager: EventManager

    def _execute(self) -> None:
        if not self.repo.is_dirty(untracked_files=True):
            return

        self.repo.git.stash('save', '-u', self.stash_name)

        self.event_manager.dispatch_event(
            GitActionWasExecuted(
                self.__class__,
                f"Changes staged in stash '{self.stash_name}'. Get it back with 'git stash pop \"{self.stash_name}\"'."
            )
        )

    def _undo(self):
        if self.stash_name is None:
            return

        self.repo.git.stash('pop', self.stash_name)
