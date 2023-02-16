from dataclasses import dataclass

from git import GitError
from injector import inject

from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mobt.GitCli.GitPython import git_logger
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

    def start(self, branch_name: BranchName, team: TeamMembers) -> SessionSettings:
        self.git.fail_if_dirty()

        try:
            if self.git.branch_exists(branch_name):
                self.git.checkout(branch_name)
                if not self.session_settings_services.find():
                    raise BranchAlreadyExistsAndIsNotMobBranch.create(branch_name)
            else:
                self.git.create_new_branch_from_main_and_checkout(branch_name)
                self.session_settings_services.create(team, RotationSettings())
                self.git.add_undo_callable(lambda: self.session_settings_services.delete())
                self.git.commit_all_and_push(
                    "WIP: mob start",
                    skip_hooks=True
                )

            return self.session_settings_services.get()
        except Exception as e:
            if self.git.undo_commands.has_commands:
                if not getattr(git_logger(), "already_logged_undo_title", False):
                    git_logger().already_logged_undo_title = True
                    git_logger().warning("Undoing all Git commands")

                self.git.undo()

            if isinstance(e, GitError):
                e = MobException(str(e))

            raise e
