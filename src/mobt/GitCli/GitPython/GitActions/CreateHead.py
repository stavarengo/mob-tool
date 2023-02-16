from dataclasses import dataclass

from git import Repo

from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.GitPython import git_logger
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass()
class CreateHead(GitAction):
    repo: Repo
    branch_name: BranchName
    main_branch: BranchName

    def _execute(self) -> None:
        git_logger().info(f'git: creating branch "{self.branch_name}" from "origin/{self.main_branch}"')
        self.repo.create_head(self.branch_name, f'origin/{self.main_branch}')

    def _undo(self):
        self.repo.git.branch("-D", self.branch_name)
