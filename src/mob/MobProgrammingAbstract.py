from abc import ABC, abstractmethod

import git

from mob.services.local_git_repo_dir import LocalGitRepoDir


class MobProgrammingAbstract(ABC):
    def __init__(self, local_git_repo_dir: LocalGitRepoDir):
        self.repo = git.Repo()

    @abstractmethod
    def start_session(self):
        pass

    @abstractmethod
    def next_driver(self):
        pass

    @abstractmethod
    def end_session(self):
        pass

    @abstractmethod
    def add_team_member(self, member: str):
        pass
