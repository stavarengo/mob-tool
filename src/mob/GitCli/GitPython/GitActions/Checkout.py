from dataclasses import dataclass

from git import Repo

from mob.GitCli.BranchName import BranchName
from mob.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass()
class Checkout(GitAction):
    repo: Repo
    branch_name: BranchName
    original_head_ref: str | None = None

    def _execute(self) -> None:
        self.original_head_ref = BranchName(
            self.original_head_ref or self.repo.active_branch.name or self.repo.active_branch.commit.hexsha
        )

        self.repo.git.checkout(self.branch_name)

    def _undo(self):
        self.repo.git.checkout(self.original_head_ref)
