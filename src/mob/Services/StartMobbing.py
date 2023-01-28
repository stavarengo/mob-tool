from dataclasses import dataclass

from mob.GitWrapper.GitWrapperAbstract import GitWrapperAbstract
from mob.Services.BranchName import BranchName


class BranchAlreadyExistsAndIsNotMobBranch(Exception):
    @classmethod
    def create(cls, branch_name: BranchName):
        return cls(f"The branch {branch_name} already exists, but it's not a mob branch yet.")


class LocalBranchIsAheadOfRemoteBranch(Exception):
    @classmethod
    def create(cls, local_branch: BranchName, remote_branch: BranchName):
        return cls(f"Local branch {local_branch} is ahead of the remote branch {remote_branch}.")


@dataclass
class StartMobbing:
    git: GitWrapperAbstract

    def start(self, branch_name: BranchName):
        self.git.checkout(branch_name)
