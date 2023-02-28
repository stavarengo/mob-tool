from dataclasses import dataclass

from git import GitError
from injector import inject

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mobt.MobApp.Exceptions import HeadIsDetached
from mobt.MobApp.MobAppRelevantOperationHappened import MobAppRelevantOperationHappened
from mobt.MobException import MobException


@inject
@dataclass
class MobWipCommit:
    git: GitCliWithAutoRollback
    event_manager: EventManager

    def next(self) -> None:
        if not self.git.current_branch():
            raise HeadIsDetached.create()

        try:
            self.git.fetch_all()

            self.git.pull_with_rebase()

            self.event_manager.dispatch_event(
                MobAppRelevantOperationHappened(f'Create WIP commit with all the local changes')
            )

            self.git.commit_all_and_push('WIP', skip_hooks=True)
        except Exception as e:
            self.git.undo()
            if isinstance(e, GitError):
                e = MobException(str(e))

            raise e
