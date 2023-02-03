from dataclasses import dataclass, field

from mob.GitCli.UndoCommands.UndoCommand import UndoCommand


@dataclass(frozen=True)
class ComposedUndoCommand(UndoCommand):
    __commands: list[UndoCommand] = field(default_factory=list)

    def undo(self):
        for command in reversed(self.__commands):
            command.undo()

    def with_command(self, command: UndoCommand) -> 'ComposedUndoCommand':
        self.__commands.append(command)
        return self

    @classmethod
    def empty(cls) -> 'UndoCommand':
        return ComposedUndoCommand()
