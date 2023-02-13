from dataclasses import dataclass

from git import Repo

from mob.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass()
class Commit(GitAction):
    repo: Repo
    message: str
    skip_hooks: bool = False

    def _execute(self) -> None:
        self.repo.git.commit('--no-verify' if self.skip_hooks else '', '-m', self.message)

    def _undo(self):
        self.repo.git.reset('HEAD^')
