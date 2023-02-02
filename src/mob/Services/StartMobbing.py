from dataclasses import dataclass

from injector import inject

from mob.GitWrapper.GitWrapperAbstract import GitWrapperAbstract, NotMobBranch, ComposedUndoCommand
from mob.MobException import MobException
from mob.Services.BranchName import BranchName
from mob.Services.MobData import MobData, MobDataTeam


class LocalBranchIsAheadOfRemoteBranch(MobException):
    @classmethod
    def create(cls, local_branch: BranchName, remote_branch: BranchName):
        return cls(f"Local branch {local_branch} is ahead of the remote branch {remote_branch}.")


class BranchAlreadyExistsAndIsNotMobBranch(MobException):
    @classmethod
    def create(cls, branch_name: BranchName):
        return cls(f"The branch {branch_name} already exists, but it's not a mob branch yet.")


@inject
@dataclass
class StartMobbing:
    git: GitWrapperAbstract
    __undo_command: ComposedUndoCommand = ComposedUndoCommand.empty()

    def start(self, branch_name: BranchName, team: list[str]):
        try:
            exists = self.git.branch_exists(branch_name)
            if exists:
                try:
                    self.__undo_command = self.__undo_command.with_command(self.git.checkout(branch_name))
                except NotMobBranch:
                    raise BranchAlreadyExistsAndIsNotMobBranch.create(branch_name)
            else:
                mob_data = MobData.create(branch_name, MobDataTeam(team.pop(), team.pop(), team))
                self.__undo_command = self.__undo_command.with_command(
                    self.git.create_new_mob_branch(branch_name, mob_data))
                self.__undo_command = self.__undo_command.with_command(self.git.checkout(branch_name))
        except Exception as e:
            self.__undo_command.undo()
            raise e
