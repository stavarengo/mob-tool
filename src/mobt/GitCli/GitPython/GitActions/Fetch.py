from dataclasses import dataclass

from git import Repo

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction
from mobt.GitCli.GitPython.GitActions.GitActionWasExecuted import GitActionWasExecuted


@dataclass()
class Fetch(GitAction):
    repo: Repo
    all: bool
    prune: bool
    event_manager: EventManager

    def _execute(self) -> None:
        options = []
        if self.all:
            options.append('--all')
        if self.prune:
            options.append('--prune')

        self.event_manager.dispatch_event(
            GitActionWasExecuted(human_log='Updating remote refs', action=Fetch)
        )

        self.repo.git.fetch(*options)

    def _undo(self):
        pass
