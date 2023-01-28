from abc import ABC, abstractmethod

from mob.Services.BranchName import BranchName


class WorkingDirectoryNotClean(Exception):
    @classmethod
    def create(cls):
        return cls("Work directory is not clean.")


class GitWrapperAbstract(ABC):

    @abstractmethod
    def is_dirty(self) -> bool:
        pass

    @abstractmethod
    def checkout(self, branch_name: BranchName):
        """
        Raises:
            WorkingDirectoryNotClean

        Args:
            branch_name:

        Returns:

        """
        pass
