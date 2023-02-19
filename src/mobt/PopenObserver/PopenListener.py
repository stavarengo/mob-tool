from dataclasses import dataclass


@dataclass
class PopenListener:

    def popen_executed(self, command: list[str], stdout: str, stderr: str) -> None:
        pass
