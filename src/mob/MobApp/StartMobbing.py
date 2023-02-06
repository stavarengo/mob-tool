from dataclasses import dataclass

from injector import inject

from mob.GitCli.BranchName import BranchName
from mob.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mob.MobApp.Exceptions import BranchAlreadyExistsAndIsNotMobBranch
from mob.SessionSettings.RotationSettings import RotationSettings
from mob.SessionSettings.SessionSettings import TeamMembers
from mob.SessionSettings.SessionSettingsService import SessionSettingsService


@inject
@dataclass
class StartMobbing:
    git: GitCliWithAutoRollback
    session_settings_services: SessionSettingsService

    def start(self, branch_name: BranchName, team: TeamMembers):
        try:
            if self.git.branch_exists(branch_name):
                self.git.checkout(branch_name)
                if self.session_settings_services.find():
                    raise BranchAlreadyExistsAndIsNotMobBranch.create(branch_name)
            else:
                self.git.create_new_branch_from_main_and_checkout(branch_name)
                self.session_settings_services.create(team, RotationSettings())
                self.git.add_undo_callable(lambda: self.session_settings_services.delete())
                self.git.commit_and_push_everything("WIP: mob start")
        except Exception as e:
            self.git.undo()
            raise e
