from abc import ABC, abstractmethod
from dataclasses import dataclass

from mob.GitCli.UndoCommands.UndoCommand import UndoCommand
from mob.Services.BranchName import BranchName
from mob.Services.MobData import MobData


@dataclass(frozen=True)
class GitCliInterface(ABC):

    @abstractmethod
    def branch_exists(self, branch_name: BranchName) -> bool:
        pass

    @abstractmethod
    def checkout(self, branch_name: BranchName, fail_if_not_mob_branch: bool = True) -> UndoCommand:
        """
        :raise: BranchAlreadyExistsAndIsNotMobBranch
        :param branch_name:
        :param fail_if_not_mob_branch:
        :return:
        """
        pass

    @abstractmethod
    def create_new_mob_branch(self, branch_name: BranchName, mob_data: MobData) -> UndoCommand:
        pass

    @abstractmethod
    def add_to_git_info_exclude(self, new_entry: str) -> UndoCommand:
        pass
