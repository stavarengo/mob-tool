from dataclasses import dataclass
from typing import Optional

import requests
from injector import inject
from packaging.version import Version

from mobt.Version import version_checker_thread_logger


@inject
@dataclass
class PyPi:

    def get_last_available_version(self) -> Optional[Version]:
        PYPI_URL = f'https://pypi.org/pypi/mob-tool/json'
        res = requests.get(PYPI_URL, timeout=5)

        if res.status_code != 200:
            version_checker_thread_logger().debug(f'PyPi response: {res.status_code}')
            return
        json = res.json()
        json_version = json['info']['version']
        version_checker_thread_logger().debug(f'PyPi response: {json_version}')

        return Version(json_version)
