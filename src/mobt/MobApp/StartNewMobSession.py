from dataclasses import dataclass
from typing import Optional

from git import GitError
from injector import inject

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mobt.MobApp.Exceptions import BranchAlreadyExistsAndIsNotMobBranch, BranchIsAlreadyAnMobBranch
from mobt.MobApp.MobAppRelevantOperationHappened import MobAppRelevantOperationHappened
from mobt.MobException import MobException
from mobt.SessionSettings import SessionSettings
from mobt.SessionSettings.RotationSettings import RotationSettings
from mobt.SessionSettings.SessionSettings import TeamMembers
from mobt.SessionSettings.SessionSettingsService import SessionSettingsService


@inject
@dataclass
class StartNewMobSession:
    git: GitCliWithAutoRollback
    event_manager: EventManager
    session_settings_services: SessionSettingsService

    def start(
        self, branch_name: Optional[BranchName], team: TeamMembers,
        force_if_non_mob_branch: bool = False, fetch_all: bool = True,
        fail_if_dirty: bool = True
    ) -> SessionSettings:
        if fail_if_dirty:
            self.git.fail_if_dirty()

        if fetch_all:
            self.git.fetch_all()

        branch_name = branch_name or self.git.current_branch()

        try:
            self._checkout_branch(branch_name, force_if_non_mob_branch)

            session_settings = self.session_settings_services.find()

            if session_settings:
                raise BranchIsAlreadyAnMobBranch.create(branch_name)

            self.event_manager.dispatch_event(MobAppRelevantOperationHappened(f'Saving mob settings file'))
            session_settings = self._create_session_settings(team)

            self.git.commit_all_and_push("WIP: Mob start!", skip_hooks=True)

            return session_settings
        except Exception as e:
            self.git.undo()

            if isinstance(e, GitError):
                e = MobException(str(e))

            raise e

    def _checkout_branch(self, branch_name: BranchName, force_if_non_mob_branch: bool) -> None:
        if not self.git.branch_exists(branch_name):
            self.git.create_new_branch_from_main_and_checkout(branch_name)
        else:
            self.git.checkout(branch_name)
            self.git.pull_with_rebase()
            if not self.session_settings_services.find() and not force_if_non_mob_branch:
                raise BranchAlreadyExistsAndIsNotMobBranch.create(branch_name)

    def _create_session_settings(self, team: TeamMembers) -> SessionSettings:
        session_settings = self.session_settings_services.create(team, RotationSettings())
        self.git.add_undo_callable(lambda: self.session_settings_services.delete())
        return session_settings
