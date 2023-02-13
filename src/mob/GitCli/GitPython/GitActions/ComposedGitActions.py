from dataclasses import dataclass, field

from mob.GitCli.GitPython import get_logger
from mob.GitCli.GitPython.GitActions.GitAction import GitAction
from mob.GitCli.UndoCommands.ComposedUndoCommand import ComposedUndoCommand

_undo_title_logged = False


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
        global _undo_title_logged
        if not _undo_title_logged:
            get_logger().warning("Undoing all Git commands")
            _undo_title_logged = True

        self.__undo.undo()

    def add_action(self, action: GitAction) -> None:
        self.__actions.append(action)
