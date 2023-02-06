from dataclasses import dataclass

from git import Repo

from mob.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass()
class Commit(GitAction):
    repo: Repo
    message: str

    def _execute(self) -> None:
        self.repo.git.commit('-m', self.message)

    def _undo(self):
        self.repo.git.reset('HEAD')
