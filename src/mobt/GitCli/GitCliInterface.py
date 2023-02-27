import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from git import Head, RemoteReference

from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.UndoCommands.UndoCommand import UndoCommand


@dataclass(frozen=True)
class GitCliInterface(ABC):
    @abstractmethod
    def current_branch(self) -> typing.Optional[BranchName]:
        pass

    @abstractmethod
    def fetch_all(self) -> UndoCommand:
        pass

    @abstractmethod
    def squash_all(self, commit_message: str, skip_hooks: bool = False) -> UndoCommand:
        pass

    @abstractmethod
    def rebase(self, log_undoing_git_commands_title: bool = True) -> UndoCommand:
        pass

    @abstractmethod
    def branch_exists(self, branch_name: BranchName) -> bool:
        pass

    @abstractmethod
    def get_local_branch(self, branch_name: BranchName) -> Optional[Head]:
        pass

    @abstractmethod
    def get_remote_branch(self, branch_name: BranchName) -> Optional[RemoteReference]:
        pass

    @abstractmethod
    def checkout(self, branch_name: BranchName) -> UndoCommand:
        """
        :raise: BranchAlreadyExistsAndIsNotMobBranch
        :param branch_name:
        :return:
        """
        pass

    @abstractmethod
    def create_new_branch_from_main_and_checkout(self, branch_name: BranchName) -> UndoCommand:
        pass

    @abstractmethod
    def push(self, force: bool = False) -> UndoCommand:
        pass

    @abstractmethod
    def commit_all(self, message: str, skip_hooks: bool = False) -> UndoCommand:
        pass

    @abstractmethod
    def add_to_git_info_exclude(self, new_entry: str) -> UndoCommand:
        pass

    @abstractmethod
    def commit_all_and_push(self, message: str, skip_hooks: bool = False) -> UndoCommand:
        pass

    @abstractmethod
    def fail_if_dirty(self):
        pass

    @abstractmethod
    def pull_with_rebase(self):
        pass
