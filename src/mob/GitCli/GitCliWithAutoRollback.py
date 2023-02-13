from dataclasses import dataclass
from typing import Callable

from injector import inject

from mob.GitCli.BranchName import BranchName
from mob.GitCli.GitCliInterface import GitCliInterface
from mob.GitCli.UndoCommands.ComposedUndoCommand import ComposedUndoCommand
from mob.GitCli.UndoCommands.UndoCallable import UndoCallable
from mob.GitCli.UndoCommands.UndoCommand import UndoCommand


@inject
@dataclass(frozen=True)
class GitCliWithAutoRollback(GitCliInterface, UndoCommand):
    git: GitCliInterface
    __undo_command: ComposedUndoCommand = ComposedUndoCommand()

    def current_branch(self) -> BranchName | None:
        return self.__call(self.git.current_branch)

    def branch_exists(self, branch_name: BranchName) -> bool:
        return self.__call(self.git.branch_exists, branch_name)

    def checkout(self, branch_name: BranchName) -> UndoCommand:
        return self.__call(self.git.checkout, branch_name)

    def fetch_all(self) -> None:
        return self.__call(self.git.checkout)

    def create_new_branch_from_main_and_checkout(self, branch_name: BranchName) -> UndoCommand:
        return self.__call(self.git.create_new_branch_from_main_and_checkout, branch_name)

    def add_to_git_info_exclude(self, new_entry: str) -> UndoCommand:
        return self.__call(self.git.add_to_git_info_exclude, new_entry)

    def commit_and_push_all(self, message: str, skip_hooks: bool = False) -> UndoCommand:
        return self.__call(self.git.commit_and_push_all, message, skip_hooks=skip_hooks)

    def undo(self):
        if self.__undo_command.has_commands:
            self.__undo_command.undo()

    def add_undo_command(self, undo_command: UndoCommand):
        self.__undo_command.add_command(undo_command)

    def add_undo_callable(self, c: callable):
        self.__undo_command.add_command(UndoCallable(c))

    @property
    def undo_commands(self) -> ComposedUndoCommand:
        return self.__undo_command

    def __call(self, method: Callable, *args, **kwargs):
        result = method(*args, **kwargs)
        if isinstance(result, UndoCommand):
            self.__undo_command.add_command(result)
        return result
