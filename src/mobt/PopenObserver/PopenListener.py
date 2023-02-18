from dataclasses import dataclass


@dataclass
class PopenListener:

    def popen_executed(self, command: list, stdout: str, stderr: str) -> None:
        pass
