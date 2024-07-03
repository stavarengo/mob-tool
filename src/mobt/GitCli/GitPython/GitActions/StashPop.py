import datetime
from dataclasses import dataclass

from git import Repo

from mobt.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass()
class StashPop(GitAction):
    repo: Repo
    stash_name: str

    def _execute(self) -> None:
        self.repo.git.stash('pop', self.stash_name)


    def _undo(self) -> None:
        self.repo.git.reset('--hard')
        self.repo.git.clean('-f', '-d')


