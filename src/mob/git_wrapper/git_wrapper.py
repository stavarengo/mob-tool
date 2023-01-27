from dataclasses import dataclass

from git import Repo

from mob.git_wrapper.git_wrapper_abstract import GitWrapperAbstract, WorkingDirectoryNotClean
from mob.services.branch_name import BranchName


@dataclass(frozen=True)
class GitWrapper(GitWrapperAbstract):
    def checkout(self, branch_name: BranchName):
        if self.repo.is_dirty():
            raise WorkingDirectoryNotClean.create()

    repo: Repo

    def is_dirty(self) -> bool:
        return self.repo.is_dirty()
