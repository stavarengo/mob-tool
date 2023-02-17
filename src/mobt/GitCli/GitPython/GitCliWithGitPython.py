import typing
from dataclasses import dataclass

from git import Repo
from injector import inject

from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.Exceptions import CanNotFindMainBranch, WorkingDirectoryNotClean
from mobt.GitCli.GitCliInterface import GitCliInterface, UndoCommand
from mobt.GitCli.GitPython.GitActions.AddAll import AddAll
from mobt.GitCli.GitPython.GitActions.AddEntryToInfoExclude import AddEntryToInfoExclude
from mobt.GitCli.GitPython.GitActions.Checkout import Checkout
from mobt.GitCli.GitPython.GitActions.Commit import Commit
from mobt.GitCli.GitPython.GitActions.ComposedGitActions import ComposedGitActions
from mobt.GitCli.GitPython.GitActions.CreateHead import CreateHead
from mobt.GitCli.GitPython.GitActions.Push import Push
from mobt.GitCli.GitPython.GitActions.SquashAll import SquashAll


@inject
@dataclass(frozen=True)
class GitCliWithGitPython(GitCliInterface):
    repo: Repo
    MOB_FILE_NAME: str = '.mobt.json'

    def current_branch(self) -> typing.Optional[BranchName]:
        if self.repo.head.is_detached:
            return None
        return BranchName(self.repo.active_branch.name)

    def fetch_all(self) -> None:
        self.repo.git.fetch('--all')

    def __get_main_branch_name(self) -> BranchName:
        all_possible_names = [BranchName('master'), BranchName('main')]
        for branch in all_possible_names:
            if branch in self.repo.remotes.origin.refs:
                return branch

        raise CanNotFindMainBranch.create(all_possible_names)

    def squash_all(self, commit_message: str, skip_hooks: bool = False) -> UndoCommand:
        return SquashAll(self.repo, self.__get_main_branch_name(), commit_message, skip_hooks).execute()

    def branch_exists(self, branch_name: BranchName) -> bool:
        return str(branch_name) in self.repo.branches or str(branch_name) in self.repo.remotes.origin.refs

    def checkout(self, branch_name: BranchName) -> UndoCommand:
        return Checkout(self.repo, branch_name).execute()

    def create_new_branch_from_main_and_checkout(self, branch_name: BranchName) -> UndoCommand:
        self.fail_if_dirty()

        return ComposedGitActions([
            CreateHead(self.repo, branch_name, self.__get_main_branch_name()),
            Checkout(self.repo, branch_name),
        ]).execute()

    def add_to_git_info_exclude(self, new_entry: str) -> UndoCommand:
        return AddEntryToInfoExclude(self.repo, new_entry).execute()

    def commit_all_and_push(self, message: str, skip_hooks: bool = False) -> UndoCommand:
        return ComposedGitActions([
            AddAll(self.repo),
            Commit(self.repo, message, skip_hooks=skip_hooks),
            Push(self.repo, BranchName(self.repo.active_branch.name)),
        ]).execute()

    def push(self, force: bool = False) -> UndoCommand:
        return Push(self.repo, BranchName(self.repo.active_branch.name), force=force).execute()

    def commit_all(self, message: str, skip_hooks: bool = False) -> UndoCommand:
        return ComposedGitActions([
            AddAll(self.repo),
            Commit(self.repo, message, skip_hooks=skip_hooks),
        ]).execute()

    def fail_if_dirty(self):
        if self.repo.is_dirty(untracked_files=True):
            raise WorkingDirectoryNotClean.create()
