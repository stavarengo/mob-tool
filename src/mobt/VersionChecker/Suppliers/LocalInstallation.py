from dataclasses import dataclass
from typing import Optional

import pkg_resources
from injector import inject
from packaging.version import Version

from mobt.VersionChecker import version_checker_logger
from mobt.VersionChecker.Suppliers.SupplierInterface import SupplierInterface


@inject
@dataclass(frozen=True)
class LocalInstallation(SupplierInterface):

    def get_version(self) -> Optional[Version]:
        version = pkg_resources.get_distribution('mob-tool').version
        version_checker_logger().debug(f'Version installed locally: {version}')

        return Version(version)
