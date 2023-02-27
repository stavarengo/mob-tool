from dataclasses import dataclass
from typing import Optional

from git import GitError
from injector import inject

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mobt.MobApp.Exceptions import BranchAlreadyExistsAndIsNotMobBranch, BranchNotFound
from mobt.MobApp.MobAppRelevantOperationHappened import MobAppRelevantOperationHappened
from mobt.MobException import MobException
from mobt.SessionSettings import SessionSettings
from mobt.SessionSettings.RotationSettings import RotationSettings
from mobt.SessionSettings.SessionSettings import TeamMembers
from mobt.SessionSettings.SessionSettingsService import SessionSettingsService


@inject
@dataclass
class ContinueMobSession:
    git: GitCliWithAutoRollback
    event_manager: EventManager
    session_settings_services: SessionSettingsService

    def go(
        self, branch_name: Optional[BranchName], team: Optional[TeamMembers],
        fetch_all: bool = True, fail_if_dirty: bool = True
    ) -> SessionSettings:
        if fail_if_dirty:
            self.git.fail_if_dirty()

        if fetch_all:
            self.git.fetch_all()

        branch_name = branch_name or self.git.current_branch()

        try:
            session_settings = self._branch_checkout(branch_name)
            if team:
                self.event_manager.dispatch_event(MobAppRelevantOperationHappened(f'Set team members to {team}'))

                session_settings = self._update_team_if_necessary(session_settings, team)
                self.git.commit_all_and_push(f"WIP: mob set team members to: {team}", skip_hooks=True)

            return session_settings
        except Exception as e:
            self.git.undo()

            if isinstance(e, GitError):
                e = MobException(str(e))

            raise e

    def _branch_checkout(self, branch_name: BranchName) -> SessionSettings:
        if not self.git.branch_exists(branch_name):
            raise BranchNotFound.create(branch_name)

        self.git.checkout(branch_name)
        self.git.pull_with_rebase()

        session_settings = self.session_settings_services.find()
        if not session_settings:
            raise BranchAlreadyExistsAndIsNotMobBranch.create(branch_name)

        return session_settings

    def _create_session_settings(self, team: TeamMembers) -> SessionSettings:
        session_settings = self.session_settings_services.create(team, RotationSettings())
        self.git.add_undo_callable(lambda: self.session_settings_services.delete())
        return session_settings

    def _update_team_if_necessary(self, current_settings: SessionSettings, new_team: TeamMembers) -> SessionSettings:
        old_team = current_settings.team
        current_settings = self.session_settings_services.update_members(new_team)
        self.git.add_undo_callable(lambda: self.session_settings_services.update_members(old_team))

        return current_settings
