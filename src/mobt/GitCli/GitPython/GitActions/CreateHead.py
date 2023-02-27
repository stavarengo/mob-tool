from dataclasses import dataclass

from git import Repo

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction
from mobt.GitCli.GitPython.GitActions.GitActionWasExecuted import GitActionWasExecuted


@dataclass()
class CreateHead(GitAction):
    repo: Repo
    branch_name: BranchName
    main_branch: BranchName
    event_manager: EventManager

    def _execute(self) -> None:
        main_tracking_branch = self.repo.branches[self.main_branch].tracking_branch()
        if not main_tracking_branch:
            return

        try:
            main_tracking_branch.commit.hexsha
        except ValueError as e:
            e_str = str(e)
            if 'Reference at' in e_str and 'does not exist' in e_str:
                return
            raise e

        self.event_manager.dispatch_event(
            GitActionWasExecuted(
                self.__class__,
                f'Creating new branch "{self.branch_name}" from "{main_tracking_branch.name}"'
            )
        )
        self.repo.create_head(self.branch_name, main_tracking_branch.name)

    def _undo(self):
        self.repo.git.branch("-D", self.branch_name)
