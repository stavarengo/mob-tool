from abc import ABC, abstractmethod
from dataclasses import dataclass

from mobt.GitCli.GitPython.GitActions.Exceptions import ActionAlreadyExecuted, ActionAlreadyUndo
from mobt.GitCli.UndoCommands.UndoCallable import UndoCallable
from mobt.GitCli.UndoCommands.UndoCommand import UndoCommand


@dataclass()
class _ExecutionControl:
    executed: bool = False
    undo: bool = False


@dataclass()
class GitAction(ABC):

    def __post_init__(self):
        self.__execution_control = _ExecutionControl()

    def execute(self) -> UndoCommand:
        if self.__execution_control.executed:
            raise ActionAlreadyExecuted.create(self.__class__.__name__)

        try:
            self._execute()
            return UndoCallable(self.undo)
        except Exception as e:
            raise e
        finally:
            self.__execution_control.executed = True

    def undo(self):
        if self.__execution_control.undo:
            raise ActionAlreadyUndo.create(self.__class__.__name__)

        try:
            self._undo()
        finally:
            self.__execution_control.undo = True

    @abstractmethod
    def _execute(self) -> None:
        pass

    def __call__(self, *args, **kwargs):
        self.execute()

    @abstractmethod
    def _undo(self):
        pass
