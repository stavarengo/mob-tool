from dataclasses import dataclass

from git import Repo

from mob.GitCli.BranchName import BranchName
from mob.GitCli.GitCliInterface import UndoCommand


@dataclass(frozen=True)
class UndoCheckout(UndoCommand):
    repo: Repo
    original_branch: BranchName

    def undo(self):
        self.repo.git.checkout(self.original_branch)
