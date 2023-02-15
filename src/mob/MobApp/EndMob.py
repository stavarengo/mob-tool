from dataclasses import dataclass

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
        self.git.fail_if_dirty()

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
        except Exception as e:
            self.git.undo()
            self.session_settings_services.create(members=session_settings.team, rotation=session_settings.rotation)
            raise e
