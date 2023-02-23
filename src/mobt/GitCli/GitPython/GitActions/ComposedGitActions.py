from dataclasses import dataclass, field

from mobt.GitCli.GitPython.GitActions.GitAction import GitAction
from mobt.GitCli.UndoCommands.ComposedUndoCommand import ComposedUndoCommand


@dataclass()
class ComposedGitActions(GitAction):
    __actions: list[GitAction] = field(default_factory=list)

    def __post_init__(self):
        self.__undo = ComposedUndoCommand()
        super().__post_init__()

    def _execute(self) -> None:
        try:
            for action in self.__actions:
                self.__undo.add_command(action.execute())
        except Exception as e:
            self.undo()
            raise e

    def _undo(self):
        self.__undo.undo()

    def add_action(self, action: GitAction) -> None:
        self.__actions.append(action)
