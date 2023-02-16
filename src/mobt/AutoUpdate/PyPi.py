from dataclasses import dataclass
from typing import Optional

import requests
from injector import inject
from packaging.version import Version

from mobt.DotEnv.DotEnv import DotEnv


@inject
@dataclass
class PyPi:
    dotEnv: DotEnv

    def get_last_available_version(self) -> Optional[Version]:
        PYPI_URL = f'https://pypi.org/pypi/{self.dotEnv.PYPI_APP_NAME}/json'
        res = requests.get(PYPI_URL, timeout=5)
        if res.status_code != 200:
            return
        json = res.json()
        return Version(json['info']['version'])
