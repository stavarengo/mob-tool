from dataclasses import dataclass

from git import Repo

from mob.GitWrapper.GitWrapperAbstract import GitWrapperAbstract, WorkingDirectoryNotClean
from mob.Services.BranchName import BranchName


@dataclass(frozen=True)
class GitWrapper(GitWrapperAbstract):
    def checkout(self, branch_name: BranchName):
        if self.repo.is_dirty():
            raise WorkingDirectoryNotClean.create()

    repo: Repo

    def is_dirty(self) -> bool:
        return self.repo.is_dirty()
