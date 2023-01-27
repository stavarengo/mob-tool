from dataclasses import dataclass

from git import Repo

from mob.git_wrapper.git_wrapper_abstract import GitWrapperAbstract


@dataclass(frozen=True)
class GitWrapper(GitWrapperAbstract):
    repo: Repo

    def is_dirty(self) -> bool:
        return self.repo.is_dirty()
