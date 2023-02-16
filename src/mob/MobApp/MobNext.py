from dataclasses import dataclass

from git import GitError
from injector import inject

from mob.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mob.GitCli.GitPython import git_logger
from mob.LastTeamMembers.TeamMemberName import TeamMemberName
from mob.MobApp.Exceptions import BranchAlreadyExistsAndIsNotMobBranch, HeadIsDetached
from mob.MobException import MobException
from mob.SessionSettings.Exceptions import SessionSettingsNotFound
from mob.SessionSettings.SessionSettingsService import SessionSettingsService


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
                'WIP: mob next\n\nHooks skipped: they will be executed when `mob end` is called',
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
                e = MobException(e)

            raise e
