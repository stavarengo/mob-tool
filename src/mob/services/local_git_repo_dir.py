import os
from dataclasses import dataclass


class InvalidGitRepoDir(Exception):
    @classmethod
    def create(cls, path: str):
        return cls(f'The directory "{path}" is not a valid repository directory.')


@dataclass(frozen=True)
class LocalGitRepoDir(os.PathLike):
    path: str

    def __post_init__(self):
        if not os.path.exists(f'{self.path}/.git'):
            raise InvalidGitRepoDir.create(self.path)

    def __fspath__(self) -> str:
        return self.path
