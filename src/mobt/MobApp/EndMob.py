from dataclasses import dataclass

from git import GitError
from injector import inject

from mobt.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mobt.MobApp.Exceptions import CurrentBranchIsNotMobBranch, HeadIsDetached
from mobt.MobException import MobException
from mobt.SessionSettings.Exceptions import SessionSettingsNotFound
from mobt.SessionSettings.SessionSettingsService import SessionSettingsService


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
            self.git.fetch_all()
            self.session_settings_services.delete()
            self.git.commit_all(
                'WIP: mob ended: session file deleted',
                skip_hooks=True
            )
            self.git.squash_all(
                'WIP: mob ended: hooks executed',
                skip_hooks=False
            )
            self.git.push(force=True)
        except Exception as e:
            self.git.undo()
            self.session_settings_services.create(members=session_settings.team, rotation=session_settings.rotation)
            if isinstance(e, GitError):
                e = MobException(str(e))
            raise e
