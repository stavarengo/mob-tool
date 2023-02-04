from dataclasses import dataclass
from typing import Callable

from injector import inject

from mob.GitCli.GitCliInterface import GitCliInterface
from mob.GitCli.UndoCommands.ComposedUndoCommand import ComposedUndoCommand
from mob.GitCli.UndoCommands.UndoCommand import UndoCommand
from mob.Services.BranchName import BranchName
from mob.Services.MobData import MobData


@inject
@dataclass(frozen=True)
class GitCliWithAutoRollback(GitCliInterface, UndoCommand):
    git: GitCliInterface
    __undo_command: ComposedUndoCommand = ComposedUndoCommand()

    def branch_exists(self, branch_name: BranchName) -> bool:
        return self.__call(self.git.branch_exists, branch_name)

    def checkout(self, branch_name: BranchName, fail_if_not_mob_branch: bool = True) -> UndoCommand:
        return self.__call(self.git.checkout, branch_name, fail_if_not_mob_branch)

    def create_new_mob_branch(self, branch_name: BranchName, mob_data: MobData) -> UndoCommand:
        return self.__call(self.git.create_new_mob_branch, branch_name, mob_data)

    def add_to_git_info_exclude(self, new_entry: str) -> UndoCommand:
        return self.__call(self.git.add_to_git_info_exclude, new_entry)

    def undo(self):
        self.__undo_command.undo()

    def __call(self, method: Callable, *args, **kwargs):
        result = method(*args, **kwargs)
        if isinstance(result, UndoCommand):
            self.__undo_command.add_command(result)
        return result
