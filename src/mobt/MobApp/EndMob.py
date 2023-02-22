import logging
from dataclasses import dataclass

from git import GitError
from injector import inject

from mobt import echo
from mobt.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mobt.Logging.color_by_log_level import color_by_log_level_int
from mobt.MobApp.Exceptions import CurrentBranchIsNotMobBranch, HeadIsDetached
from mobt.MobException import MobException
from mobt.SessionSettings.Exceptions import SessionSettingsNotFound
from mobt.SessionSettings.SessionSettingsService import SessionSettingsService


@inject
@dataclass
class EndMob:
    git: GitCliWithAutoRollback

    session_settings_services: SessionSettingsService

    def end(self, message: str = None, do_not_try_to_rebase: bool = False):
        self.git.fail_if_dirty()

        current_branch_name = self.git.current_branch()
        if not current_branch_name:
            raise HeadIsDetached.create()

        try:
            session_settings = self.session_settings_services.get()
        except SessionSettingsNotFound:
            raise CurrentBranchIsNotMobBranch.create(current_branch_name)

        try:
            self.git.fetch_all()
            self.session_settings_services.delete()
            self.git.commit_all('WIP: Mob done! Session file deleted.', skip_hooks=True)
            self.git.squash_all(message or 'WIP: Mob done! Squash all and execute hooks.', skip_hooks=False)
            if not do_not_try_to_rebase:
                try:
                    self.git.with_manual_roll_back().rebase(log_undoing_git_commands_title=False)
                except GitError as e:
                    echo(f" > Can't perform auto-rebase. You should do it manually.",
                         fg=color_by_log_level_int(logging.INFO))
                    echo(f" > This does not affect the mob ending in any way.", fg=color_by_log_level_int(logging.INFO))
                    echo(f" > To avoid trying auto-rebase during `mobt done`, use the option `-R` next time.",
                         fg=color_by_log_level_int(logging.INFO))

            self.git.push(force=True)
        except Exception as e:
            self.git.undo()
            self.session_settings_services.create(members=session_settings.team, rotation=session_settings.rotation)
            if isinstance(e, GitError):
                e = MobException(str(e))
            raise e
