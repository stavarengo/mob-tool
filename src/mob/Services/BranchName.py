import re
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True, eq=True)
class BranchName:
    branch_name: str

    def __post_init__(self):
        pattern = re.compile("^[a-zA-Z0-9_.-]+$")
        if not pattern.match(self.branch_name):
            raise ValueError(f"Invalid branch name: {self.branch_name}")

    def __fspath__(self):
        """Return the file system path representation of the object."""
        raise self.branch_name

    def __str__(self):
        return self.branch_name

    def __eq__(self, other):
        if isinstance(other, BranchName):
            return self.branch_name == other.branch_name
        return False
