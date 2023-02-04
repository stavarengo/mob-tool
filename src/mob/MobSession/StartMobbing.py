from dataclasses import dataclass

from injector import inject

from mob.GitCli.Exceptions import NotMobBranch
from mob.GitCli.GitCliInterface import GitCliInterface
from mob.GitCli.UndoCommands.ComposedUndoCommand import ComposedUndoCommand
from mob.MobSession.Exceptions import BranchAlreadyExistsAndIsNotMobBranch
from mob.Services.BranchName import BranchName
from mob.Services.MobData import MobData, TeamMembers


@inject
@dataclass
class StartMobbing:
    git: GitCliInterface
    __undo_command: ComposedUndoCommand = ComposedUndoCommand.empty()

    def start(self, branch_name: BranchName, team: TeamMembers):
        try:
            exists = self.git.branch_exists(branch_name)
            if exists:
                try:
                    self.__undo_command = self.__undo_command.with_command(self.git.checkout(branch_name))
                except NotMobBranch:
                    raise BranchAlreadyExistsAndIsNotMobBranch.create(branch_name)
            else:
                mob_data = MobData.create(branch_name, TeamMembers(team.pop(), team.pop(), team))
                self.__undo_command = self.__undo_command.with_command(
                    self.git.create_new_mob_branch(branch_name, mob_data))
                self.__undo_command = self.__undo_command.with_command(self.git.checkout(branch_name))
        except Exception as e:
            self.__undo_command.undo()
            raise e
