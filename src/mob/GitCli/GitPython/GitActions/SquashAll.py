from dataclasses import dataclass

from git import Repo

from mob.GitCli.BranchName import BranchName
from mob.GitCli.Exceptions import ThereIsNoDifferenceBetweenTheCurrentBranchAndTheMainBranch
from mob.GitCli.GitPython.GitActions.AddAll import AddAll
from mob.GitCli.GitPython.GitActions.Commit import Commit
from mob.GitCli.GitPython.GitActions.ComposedGitActions import ComposedGitActions
from mob.GitCli.GitPython.GitActions.GitAction import GitAction
from mob.GitCli.GitPython.GitActions.Reset import Reset


@dataclass(frozen=False)
class _FailIfNotDirty(GitAction):
    repo: Repo
    active_branch: BranchName
    main_branch: BranchName

    def _execute(self) -> None:
        if not self.repo.is_dirty():
            raise ThereIsNoDifferenceBetweenTheCurrentBranchAndTheMainBranch.create(
                self.active_branch,
                self.main_branch
            )

    def _undo(self):
        pass


@dataclass(frozen=False)
class _Context:
    start_hash: str = None


@dataclass()
class SquashAll(GitAction):
    repo: Repo
    main_branch: BranchName
    commit_message: str
    skip_hooks: bool = False

    def __post_init__(self):
        self.__context: _Context = _Context()
        super().__post_init__()

    def _execute(self) -> None:
        active_branch = self.repo.active_branch

        # Find the common ancestor of the feature branch and the master branch
        master = self.repo.heads[self.main_branch]
        base = self.repo.merge_base(active_branch, master).pop()

        self.__commands = ComposedGitActions([
            Reset(self.repo, BranchName(str(base)), hard=False),
            _FailIfNotDirty(self.repo, BranchName(active_branch.name), self.main_branch),
            AddAll(self.repo),
            Commit(self.repo, self.commit_message, skip_hooks=self.skip_hooks),
        ])

        self.__commands.execute()

    def _undo(self):
        if self.__commands:
            self.__commands.undo()
