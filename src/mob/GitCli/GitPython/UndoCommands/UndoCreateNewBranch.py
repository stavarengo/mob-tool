from dataclasses import dataclass

from git import GitCommandError, Repo

from mob.GitCli.GitCliInterface import UndoCommand
from mob.Services.BranchName import BranchName


@dataclass(frozen=True)
class UndoCreateNewBranch(UndoCommand):
    repo: Repo
    branch_name: BranchName

    def undo(self):
        try:
            self.repo.git.push("origin", "--delete", self.branch_name)
        except GitCommandError as e:
            if "remote ref does not exist" not in str(e):
                raise e
        self.repo.git.branch("-D", self.branch_name)
