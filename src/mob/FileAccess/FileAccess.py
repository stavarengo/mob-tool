import os
import typing
from dataclasses import dataclass

from injector import inject


@inject
@dataclass
class FileAccess:

    def read(self, file_path: str, fail_if_not_found: bool = False) -> typing.Optional[str]:
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except FileNotFoundError as e:
            if fail_if_not_found:
                raise e
            return None

    def save(self, content: str, file_path: str) -> None:
        with open(file_path, 'w') as f:
            f.write(content)

    def delete(self, file_path: str) -> None:
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass
