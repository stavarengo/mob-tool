import os
from dataclasses import dataclass

from dotenv import load_dotenv
from injector import inject


def _load_dotenv() -> None:
    if _load_dotenv.__loaded:
        return
    load_dotenv()
    _load_dotenv.__loaded = True


_load_dotenv.__loaded = False


@inject
@dataclass(frozen=True)
class DotEnv:
    def __init__(self):
        _load_dotenv()

    @property
    def PYPI_APP_NAME(self) -> str:
        return os.getenv('PYPI_APP_NAME')

    @property
    def APP_ENV(self) -> str:
        return os.getenv('APP_ENV')

    def is_development(self) -> bool:
        return self.APP_ENV == 'dev'
