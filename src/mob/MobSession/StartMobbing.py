from dataclasses import dataclass

from injector import inject

from mob.GitCli.Exceptions import NotMobBranch
from mob.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mob.MobSession.Exceptions import BranchAlreadyExistsAndIsNotMobBranch
from mob.Services.BranchName import BranchName
from mob.Services.MobData import MobData, TeamMembers


@inject
@dataclass
class StartMobbing:
    git: GitCliWithAutoRollback

    def start(self, branch_name: BranchName, team: TeamMembers):
        try:
            if self.git.branch_exists(branch_name):
                self.git.checkout(branch_name)
            else:
                mob_data = MobData.create(branch_name, team)
                self.git.create_new_mob_branch(branch_name, mob_data)
                self.git.checkout(branch_name)
        except NotMobBranch:
            raise BranchAlreadyExistsAndIsNotMobBranch.create(branch_name)
        except Exception as e:
            self.git.undo()
            raise e

        self.git.undo()
