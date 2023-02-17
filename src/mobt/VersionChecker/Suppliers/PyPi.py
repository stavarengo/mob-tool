from dataclasses import dataclass
from typing import Optional

import requests
from injector import inject
from packaging.version import Version

from mobt.VersionChecker import version_checker_logger
from mobt.VersionChecker.Suppliers.SupplierInterface import SupplierInterface

_PYPI_URL = f'https://pypi.org/pypi/mob-tool/json'


@inject
@dataclass(frozen=True)
class PyPi(SupplierInterface):

    def get_version(self) -> Optional[Version]:
        res = requests.get(_PYPI_URL, timeout=5)

        if res.status_code != 200:
            version_checker_logger().debug(f'PyPi response: {res.status_code}')
            return None

        json = res.json()
        json_version = json['info']['version']
        version_checker_logger().debug(f'PyPi response: {json_version}')

        return Version(json_version)
