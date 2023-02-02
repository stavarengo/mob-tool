from abc import ABC, abstractmethod
from dataclasses import field, dataclass

from mob.MobException import MobException
from mob.Services.BranchName import BranchName
from mob.Services.MobData import MobData


class WorkingDirectoryNotClean(MobException):
    @classmethod
    def create(cls):
        return cls("Work directory is not clean.")


class LocalBranchIsAheadOfRemoteBranch(MobException):
    pass

    @classmethod
    def create(cls, local_branch: BranchName, remote_branch: BranchName):
        return cls(f'Branch "{local_branch}" is ahead of "{remote_branch}".')


class NotMobBranch(MobException):
    pass

    @classmethod
    def create(cls, branch_name: BranchName):
        return cls(f'Branch "{branch_name}" is not a mob branch.')


@dataclass(frozen=True)
class UndoCommand(ABC):
    def undo(self):
        pass

    def __call__(self, *args, **kwargs):
        self.undo()

    @classmethod
    def empty(cls) -> 'UndoCommand':
        return UndoCommand()


@dataclass(frozen=True)
class ComposedUndoCommand(UndoCommand):
    __commands: list[UndoCommand] = field(default_factory=list)

    def undo(self):
        for command in reversed(self.__commands):
            command.undo()

    def with_command(self, command: UndoCommand) -> 'ComposedUndoCommand':
        self.__commands.append(command)
        return self

    @classmethod
    def empty(cls) -> 'UndoCommand':
        return ComposedUndoCommand()


@dataclass(frozen=True)
class GitWrapperAbstract(ABC):

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
