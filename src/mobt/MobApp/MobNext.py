from dataclasses import dataclass

from git import GitError
from injector import inject

from mobt.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mobt.GitCli.GitPython import git_logger
from mobt.LastTeamMembers.TeamMemberName import TeamMemberName
from mobt.MobApp.Exceptions import BranchAlreadyExistsAndIsNotMobBranch, HeadIsDetached
from mobt.MobException import MobException
from mobt.SessionSettings.Exceptions import SessionSettingsNotFound
from mobt.SessionSettings.SessionSettingsService import SessionSettingsService


@inject
@dataclass
class MobNext:
    git: GitCliWithAutoRollback

    session_settings_services: SessionSettingsService

    def next(self) -> TeamMemberName:
        if not self.git.current_branch():
            raise HeadIsDetached.create()

        try:
            try:
                old_session = self.session_settings_services.get()
                new_session = self.session_settings_services.update_members(old_session.team.rotate())
                self.git.add_undo_callable(lambda: self.session_settings_services.update_members(old_session.team))
            except SessionSettingsNotFound:
                raise BranchAlreadyExistsAndIsNotMobBranch.create(self.git.current_branch())

            self.git.fetch_all()

            self.git.commit_all_and_push(
                'WIP: mob next',
                skip_hooks=True
            )

            return new_session.team.driver
        except Exception as e:
            if self.git.undo_commands.len > 1:
                if not getattr(git_logger(), "already_logged_undo_title", False):
                    git_logger().already_logged_undo_title = True
                    git_logger().warning("Undoing all Git commands")

            self.git.undo()
            if isinstance(e, GitError):
                e = MobException(str(e))

            raise e
