from dataclasses import dataclass

from git import Repo

from mob.GitCli.BranchName import BranchName
from mob.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass()
class CreateHead(GitAction):
    repo: Repo
    branch_name: BranchName

    def _execute(self) -> None:
        self.repo.create_head(self.branch_name, f'origin/{self.__get_main_branch_name()}')

    def _undo(self):
        self.repo.git.branch("-D", self.branch_name)

    def __get_main_branch_name(self) -> BranchName | None:
        all_possible_names = ['master', 'main']
        for branch in all_possible_names:
            if branch in self.repo.remotes.origin.refs:
                return BranchName(branch)

        return None
