from dataclasses import dataclass

from git import Repo

from mobt.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass()
class AddAll(GitAction):
    repo: Repo

    def __post_init__(self):
        super().__post_init__()
        self.__nothing_to_add = False

    def _execute(self) -> None:
        if not self.repo.is_dirty(untracked_files=True):
            self.__nothing_to_add = True
            return

        self.repo.git.add('-A')

    def _undo(self):
        if self.__nothing_to_add:
            return
        
        self.repo.git.reset()
