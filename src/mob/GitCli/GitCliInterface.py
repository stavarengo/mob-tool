from abc import ABC, abstractmethod
from dataclasses import dataclass

from mob.GitCli.BranchName import BranchName
from mob.GitCli.UndoCommands.UndoCommand import UndoCommand


@dataclass(frozen=True)
class GitCliInterface(ABC):
    @abstractmethod
    def current_branch(self) -> BranchName | None:
        pass

    @abstractmethod
    def fetch_all(self) -> None:
        pass

    @abstractmethod
    def branch_exists(self, branch_name: BranchName) -> bool:
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
    def add_to_git_info_exclude(self, new_entry: str) -> UndoCommand:
        pass

    def commit_and_push_everything(self, message: str, skip_hooks: bool = False) -> UndoCommand:
        pass
