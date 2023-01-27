import re
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class BranchName:
    branch_name: str

    def __post_init__(self):
        pattern = re.compile("^[a-zA-Z0-9_.-]+$")
        if not pattern.match(self.branch_name):
            raise ValueError(f"Invalid branch name: {self.branch_name}")
