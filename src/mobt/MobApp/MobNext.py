from dataclasses import dataclass

from git import GitError
from injector import inject

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mobt.MobApp.Exceptions import BranchAlreadyExistsAndIsNotMobBranch, HeadIsDetached
from mobt.MobApp.MobAppRelevantOperationHappened import MobAppRelevantOperationHappened
from mobt.MobException import MobException
from mobt.SessionSettings.Exceptions import SessionSettingsNotFound
from mobt.SessionSettings.SessionSettings import SessionSettings
from mobt.SessionSettings.SessionSettingsService import SessionSettingsService


@inject
@dataclass
class MobNext:
    git: GitCliWithAutoRollback
    event_manager: EventManager
    session_settings_services: SessionSettingsService

    def next(self) -> SessionSettings:
        if not self.git.current_branch():
            raise HeadIsDetached.create()

        try:
            self.git.fetch_all()

            self.git.pull_with_rebase()

            try:
                self.event_manager.dispatch_event(MobAppRelevantOperationHappened(f'Set new driver'))

                old_session = self.session_settings_services.get()
                self.session_settings_services.update_members(old_session.team.rotate())
                self.git.add_undo_callable(lambda: self.session_settings_services.update_members(old_session.team))
                new_session = self.session_settings_services.inc_rotation_count()
                self.git.add_undo_callable(lambda: self.session_settings_services.inc_rotation_count(-1))
            except SessionSettingsNotFound:
                raise BranchAlreadyExistsAndIsNotMobBranch.create(self.git.current_branch())

            self.event_manager.dispatch_event(MobAppRelevantOperationHappened(f'Commit and changes'))

            self.git.commit_all_and_push(
                f'WIP: Mob next! Driver: {new_session.team.driver}, nav: {new_session.team.navigator}', skip_hooks=True
            )

            return new_session
        except Exception as e:
            self.git.undo()
            if isinstance(e, GitError):
                e = MobException(str(e))

            raise e
