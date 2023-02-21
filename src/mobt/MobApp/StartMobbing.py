from dataclasses import dataclass
from typing import Optional

from git import GitError
from injector import inject

from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mobt.GitCli.GitPython import log_undoing_all_git_commands
from mobt.MobApp.Exceptions import BranchAlreadyExistsAndIsNotMobBranch
from mobt.MobException import MobException
from mobt.SessionSettings import SessionSettings
from mobt.SessionSettings.RotationSettings import RotationSettings
from mobt.SessionSettings.SessionSettings import TeamMembers
from mobt.SessionSettings.SessionSettingsService import SessionSettingsService
from mobt.Timer.TimerService import TimerService


@inject
@dataclass
class StartMobbing:
    git: GitCliWithAutoRollback

    session_settings_services: SessionSettingsService

    timer: TimerService

    def start(self, branch_name: Optional[BranchName], team: TeamMembers,
              force_if_non_mob_branch: bool = False) -> SessionSettings:
        self.git.fail_if_dirty()

        branch_name = branch_name or self.git.current_branch()

        try:
            self._switch_to_the_right_branch(branch_name, force_if_non_mob_branch)

            session_settings = self.session_settings_services.find()
            if session_settings:
                session_settings = self._update_team_if_necessary(session_settings, team)
            else:
                session_settings = self._create_session_settings(team)

            self.git.commit_all_and_push("WIP: mob start", skip_hooks=True)

            return session_settings
        except Exception as e:
            if self.git.undo_commands.has_commands:
                log_undoing_all_git_commands()
                self.git.undo()

            if isinstance(e, GitError):
                e = MobException(str(e))

            raise e

    def _switch_to_the_right_branch(self, branch_name: BranchName, force_if_non_mob_branch: bool) -> None:
        if not self.git.branch_exists(branch_name):
            self.git.create_new_branch_from_main_and_checkout(branch_name)
        else:
            self.git.checkout(branch_name)
            session_settings = self.session_settings_services.find()
            if session_settings:
                self.git.pull_with_rebase()

            session_settings = self.session_settings_services.find()
            if not session_settings:
                if force_if_non_mob_branch:
                    self.git.pull_with_rebase()
                else:
                    raise BranchAlreadyExistsAndIsNotMobBranch.create(branch_name)

    def _create_session_settings(self, team: TeamMembers) -> SessionSettings:
        session_settings = self.session_settings_services.create(team, RotationSettings())
        self.git.add_undo_callable(lambda: self.session_settings_services.delete())
        return session_settings

    def _update_team_if_necessary(self, current_settings: SessionSettings, new_team: TeamMembers) -> SessionSettings:
        old_team = current_settings.team
        if old_team != new_team:
            current_settings = self.session_settings_services.update_members(new_team)
            self.git.add_undo_callable(lambda: self.session_settings_services.update_members(old_team))

        return current_settings
