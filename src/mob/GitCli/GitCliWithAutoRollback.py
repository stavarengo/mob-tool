from dataclasses import dataclass
from typing import Callable

from injector import inject

from mob.GitCli.BranchName import BranchName
from mob.GitCli.GitCliInterface import GitCliInterface
from mob.GitCli.UndoCommands.ComposedUndoCommand import ComposedUndoCommand
from mob.GitCli.UndoCommands.UndoCommand import UndoCommand


@inject
@dataclass(frozen=True)
class GitCliWithAutoRollback(GitCliInterface, UndoCommand):
    git: GitCliInterface
    __undo_command: ComposedUndoCommand = ComposedUndoCommand()

    def branch_exists(self, branch_name: BranchName) -> bool:
        return self.__call(self.git.branch_exists, branch_name)

    def checkout(self, branch_name: BranchName, fail_if_not_mob_branch: bool = True) -> UndoCommand:
        return self.__call(self.git.checkout, branch_name, fail_if_not_mob_branch)

    def create_new_branch_from_main_and_checkout(self, branch_name: BranchName) -> UndoCommand:
        return self.__call(self.git.create_new_branch_from_main_and_checkout, branch_name)

    def add_to_git_info_exclude(self, new_entry: str) -> UndoCommand:
        return self.__call(self.git.add_to_git_info_exclude, new_entry)

    def commit_and_push_everything(self, message: str) -> UndoCommand:
        return self.__call(self.git.commit_and_push_everything, message)

    def undo(self):
        self.__undo_command.undo()

    def __call(self, method: Callable, *args, **kwargs):
        result = method(*args, **kwargs)
        if isinstance(result, UndoCommand):
            self.__undo_command.add_command(result)
        return result
