from dataclasses import dataclass

from git import Repo

from mob.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass()
class AddAll(GitAction):
    repo: Repo

    def _execute(self) -> None:
        self.repo.git.add('-A')

    def _undo(self):
        self.repo.git.reset()
