from dataclasses import dataclass

from git import Repo

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.Exceptions import ThereIsNoDifferenceBetweenTheCurrentBranchAndTheMainBranch
from mobt.GitCli.GitPython.GitActions.AddAll import AddAll
from mobt.GitCli.GitPython.GitActions.Commit import Commit
from mobt.GitCli.GitPython.GitActions.ComposedGitActions import ComposedGitActions
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction
from mobt.GitCli.GitPython.GitActions.GitActionWasExecuted import GitActionWasExecuted
from mobt.GitCli.GitPython.GitActions.Reset import Reset


@dataclass(frozen=False)
class _FailIfNotDirty(GitAction):
    repo: Repo
    active_branch: BranchName
    main_branch: BranchName
    event_manager: EventManager

    def _execute(self) -> None:
        if not self.repo.is_dirty(untracked_files=True):
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
    event_manager: EventManager
    skip_hooks: bool = False

    def __post_init__(self):
        self.__context: _Context = _Context()
        super().__post_init__()

    def _execute(self) -> None:
        active_branch = self.repo.active_branch

        # Find the common ancestor of the feature branch and the master branch
        master = self.repo.remotes.origin.refs[self.main_branch]
        base = self.repo.merge_base(active_branch, master).pop()

        self.event_manager.dispatch_event(GitActionWasExecuted(self.__class__, 'Squashing all commits into one'))

        self.__commands = ComposedGitActions(
            [
                Reset(self.repo, BranchName(str(base)), hard=False),
                _FailIfNotDirty(
                    self.repo,
                    BranchName(active_branch.name),
                    self.main_branch,
                    event_manager=self.event_manager
                ),
                AddAll(self.repo),
                Commit(self.repo, self.commit_message, skip_hooks=self.skip_hooks),
            ]
        )

        self.__commands.execute()

    def _undo(self):
        if self.__commands:
            self.__commands.undo()
