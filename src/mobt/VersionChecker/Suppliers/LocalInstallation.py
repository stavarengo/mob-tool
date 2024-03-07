from dataclasses import dataclass
from typing import Optional

# Updated imports
from importlib.metadata import version, PackageNotFoundError
from injector import inject
from packaging.version import Version

from mobt.VersionChecker import version_checker_logger
from mobt.VersionChecker.Suppliers.SupplierInterface import SupplierInterface

@inject
@dataclass(frozen=True)
class LocalInstallation(SupplierInterface):

    def get_version(self) -> Optional[Version]:
        try:
            # Using importlib.metadata.version to get the package version
            version_str = version('mob-tool')
            version_checker_logger().debug(f'Version installed locally: {version_str}')

            return Version(version_str)
        except PackageNotFoundError:
            # Handle the case where the package is not found
            version_checker_logger().debug('mob-tool package not found locally.')
            return None
