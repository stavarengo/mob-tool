from dataclasses import dataclass
from typing import Optional

import requests
from injector import inject
from packaging.version import Version


@inject
@dataclass
class PyPi:

    def get_last_available_version(self) -> Optional[Version]:
        PYPI_URL = f'https://pypi.org/pypi/mob-tool/json'
        res = requests.get(PYPI_URL, timeout=5)
        if res.status_code != 200:
            return
        json = res.json()
        return Version(json['info']['version'])
