from dataclasses import dataclass, field

from mob.GitCli.UndoCommands.UndoCommand import UndoCommand


@dataclass(frozen=True)
class ComposedUndoCommand(UndoCommand):
    __commands: list[UndoCommand] = field(default_factory=list)

    def undo(self):
        for command in reversed(self.__commands):
            command.undo()

        self.__commands.clear()

    def add_command(self, command: UndoCommand) -> 'ComposedUndoCommand':
        self.__commands.append(command)
        return self

    @property
    def has_commands(self) -> bool:
        return len(self.__commands) > 0

    @property
    def len(self) -> int:
        return len(self.__commands)

    @classmethod
    def empty(cls) -> 'UndoCommand':
        return ComposedUndoCommand()
