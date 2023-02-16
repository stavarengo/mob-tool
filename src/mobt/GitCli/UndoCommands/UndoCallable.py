from dataclasses import dataclass

from mobt.GitCli.UndoCommands.UndoCommand import UndoCommand


@dataclass(frozen=True)
class UndoCallable(UndoCommand):
    c: callable

    def undo(self):
        self.c()

    def __call__(self, *args, **kwargs):
        self.undo()
