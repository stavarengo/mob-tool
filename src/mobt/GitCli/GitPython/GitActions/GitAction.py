from abc import ABC, abstractmethod
from dataclasses import dataclass

from git import GitCommandError

from mobt.GitCli.GitPython import git_logger
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
            raise ActionAlreadyExecuted.create(self)

        try:
            self._execute()
            return UndoCallable(self.undo)
        except Exception as e:
            if not getattr(e, "already_logged", False):
                e.already_logged = True
                msg = str(e)
                if isinstance(e, GitCommandError):
                    stderr = (e.stderr and e.stderr.strip() or "").removeprefix("stderr: ").strip("'")
                    max_stderr_len = 40
                    if len(stderr) > max_stderr_len:
                        stderr = stderr.replace("\n", " ")[:max_stderr_len] + "..."
                    msg = f'Git command failed with exit code "{e.status}" and stderr "{stderr}"'

                git_logger().error(f"Failed: {msg}")
            raise e
        finally:
            self.__execution_control.executed = True

    def undo(self):
        if self.__execution_control.undo:
            raise ActionAlreadyUndo.create(self)

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
