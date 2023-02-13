from dataclasses import dataclass

import click
from injector import inject

from mob.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mob.MobApp.Exceptions import CurrentBranchIsNotMobBranch, HeadIsDetached
from mob.SessionSettings.Exceptions import SessionSettingsNotFound
from mob.SessionSettings.SessionSettingsService import SessionSettingsService


@inject
@dataclass
class EndMob:
    git: GitCliWithAutoRollback

    session_settings_services: SessionSettingsService

    def end(self):
        current_branch_name = self.git.current_branch()
        if not current_branch_name:
            raise HeadIsDetached.create()

        try:
            session_settings = self.session_settings_services.get()
        except SessionSettingsNotFound:
            raise CurrentBranchIsNotMobBranch.create(current_branch_name)

        try:
            self.session_settings_services.delete()
            self.git.commit_all(
                f'WIP: mob done: delete session file\n\nHooks skipped: they will be executed when `mob end` is called',
                skip_hooks=True
            )
            self.git.squash_all(
                f'WIP: mob done\n\nHooks executed',
                skip_hooks=False
            )
            self.git.push(force=True)

            print(click.style(f'Done!'))
        except Exception as e:
            # if self.git.undo_commands.len > 1:
            #     get_logger().warning("Undoing all Git commands")
            self.git.undo()
            self.session_settings_services.create(members=session_settings.team, rotation=session_settings.rotation)
            raise e
