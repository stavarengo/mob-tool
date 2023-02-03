from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class UndoCommand(ABC):
    def undo(self):
        pass

    def __call__(self, *args, **kwargs):
        self.undo()

    @classmethod
    def empty(cls) -> 'UndoCommand':
        return UndoCommand()
