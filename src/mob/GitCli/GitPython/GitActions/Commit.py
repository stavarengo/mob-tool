from dataclasses import dataclass

from git import Repo

from mob.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass()
class Commit(GitAction):
    repo: Repo
    message: str
    skip_hooks: bool = False

    def _execute(self) -> None:
        if self.skip_hooks:
            self.repo.git.commit('--no-verify', '-m', self.message)
        else:
            self.repo.git.commit('-m', self.message)

    def _undo(self):
        self.repo.git.reset('HEAD^')
