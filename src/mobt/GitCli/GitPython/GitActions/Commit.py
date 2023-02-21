from dataclasses import dataclass

from git import Repo

from mobt.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass()
class Commit(GitAction):
    repo: Repo
    message: str
    skip_hooks: bool = False

    def __post_init__(self):
        super().__post_init__()
        self.__nothing_to_commit = False

    def _execute(self) -> None:
        if not self.repo.is_dirty(untracked_files=True):
            self.__nothing_to_commit = True
            return

        if self.skip_hooks:
            self.repo.git.commit('--no-verify', '-m', self.message)
        else:
            self.repo.git.commit('-m', self.message)

    def _undo(self):
        if self.__nothing_to_commit:
            return
        self.repo.git.reset('HEAD^')
