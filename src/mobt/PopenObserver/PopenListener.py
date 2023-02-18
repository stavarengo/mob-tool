from dataclasses import dataclass


@dataclass
class PopenListener:

    def popen_executed(self, command: str, stdout: str, stderr: str) -> None:
        pass
