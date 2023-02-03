from dataclasses import dataclass

from git import Repo

from mob.GitCli.GitCliInterface import UndoCommand
from mob.Services.BranchName import BranchName


@dataclass(frozen=True)
class UndoCreateHead(UndoCommand):
    repo: Repo
    branch_name: BranchName

    def undo(self):
        self.repo.git.branch("-D", self.branch_name)
