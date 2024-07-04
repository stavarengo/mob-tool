import datetime
from dataclasses import dataclass

from git import Repo

from mobt import echo
from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.GitPython.GitActions.Exceptions import StashNameAreadyExists
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction
from mobt.GitCli.GitPython.GitActions.GitActionWasExecuted import GitActionWasExecuted
from mobt.GitCli.GitPython.GitActions.shared.find_stash_index_by_name import find_stash_index_by_name


@dataclass()
class StashIfDirty(GitAction):
    repo: Repo
    stash_name: str
    event_manager: EventManager

    def _execute(self) -> None:
        if not self.repo.is_dirty(untracked_files=True):
            return

        if find_stash_index_by_name(self.repo, self.stash_name) is not None:
            raise StashNameAreadyExists.create(self.stash_name)

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

        stash_index = find_stash_index_by_name(self.repo, self.stash_name)
        if stash_index is None:
            echo(f"Could not find stash with name '{self.stash_name}' to pop.", fg='bright_red')

        self.repo.git.stash('pop', f'stash@{{{stash_index}}}')
