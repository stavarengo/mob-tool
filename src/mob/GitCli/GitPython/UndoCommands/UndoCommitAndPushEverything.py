from dataclasses import dataclass

from git import Repo

from mob.GitCli.GitCliInterface import UndoCommand


@dataclass(frozen=True)
class UndoCommitAndPushEverything(UndoCommand):
    repo: Repo

    def undo(self):
        self.repo.git.reset('HEAD^ --soft')
        self.repo.git.push("-f")
