import logging
from dataclasses import dataclass
from typing import Optional

from git import GitError
from injector import inject

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.Exceptions import WorkingDirectoryNotClean
from mobt.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mobt.MobApp.Exceptions import CurrentBranchIsNotMobBranch, HeadIsDetached
from mobt.MobApp.MobAppRelevantOperationHappened import MobAppRelevantOperationHappened
from mobt.MobException import MobException
from mobt.SessionSettings.Exceptions import SessionSettingsNotFound
from mobt.SessionSettings.SessionSettingsService import SessionSettingsService


@inject
@dataclass
class SquashBranch:
    git: GitCliWithAutoRollback
    event_manager: EventManager
    session_settings_services: SessionSettingsService

    def squash(self, branch_name: Optional[BranchName], message: str = None, do_not_try_to_rebase: bool = False, push: bool = False):
        if not branch_name:
            branch_name = self.git.current_branch()
            if not branch_name:
                raise HeadIsDetached.create()

        try:
            self.git.fetch_all()

            if branch_name != self.git.current_branch():
                try:
                    self.git.fail_if_dirty()
                except WorkingDirectoryNotClean as e:
                    self.event_manager.dispatch_event(
                        MobAppRelevantOperationHappened(
                            human_log=f"Can't checkout {branch_name} because working directory is dirty.",
                            level=logging.ERROR,
                        )
                    )
                    raise e

                self.git.checkout(branch_name)

            self.git.pull_with_rebase()
            self.git.commit_all('WIP: Mob squash! Session file deleted.', skip_hooks=True)
            self.git.squash_all(message or 'Mob Squash all and execute hooks.', skip_hooks=False)
            if not do_not_try_to_rebase:
                try:
                    self.git.with_manual_roll_back().rebase(log_undoing_git_commands_title=False)
                except GitError:
                    human_log = f" > Can't auto-rebase back on top of main branch. You should do it manually."

                    self.event_manager.dispatch_event(
                        MobAppRelevantOperationHappened(human_log=human_log, level=logging.WARNING)
                    )

            if push:
                self.git.push(force=True)
        except Exception as e:
            self.git.undo()
            if isinstance(e, GitError):
                e = MobException(str(e))
            raise e
