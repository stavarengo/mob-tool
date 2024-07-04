from dataclasses import dataclass

from git import Repo

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction
from mobt.GitCli.GitPython.GitActions.GitActionWasExecuted import GitActionWasExecuted


@dataclass()
class PermanentlyCleanWorkingDirectory(GitAction):
    repo: Repo
    event_manager: EventManager

    def _execute(self) -> None:
        self.repo.git.reset('--hard')
        self.repo.git.clean('-f', '-d')

        self.event_manager.dispatch_event(
            GitActionWasExecuted(
                self.__class__,
                f"You workdir is not clean. All changes in the workdir were reverted. This is not reversible."
            )
        )

    def _undo(self) -> None:
        pass


