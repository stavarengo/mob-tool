from dataclasses import dataclass

from git import Repo, GitCommandError

from mob.GitWrapper.GitWrapperAbstract import GitWrapperAbstract, WorkingDirectoryNotClean, NotMobBranch, UndoCommand, \
    ComposedUndoCommand
from mob.MobException import MobException
from mob.Services.BranchName import BranchName
from mob.Services.MobData import MobData


class MainBranchNotFound(MobException):
    @classmethod
    def create(cls, branch_names: list[BranchName]):
        return cls(f"Main branch not found. We tried branches named: {', '.join([str(bn) for bn in branch_names])}.")


@dataclass(frozen=True)
class UndoCheckout(UndoCommand):
    repo: Repo
    original_branch: BranchName

    def undo(self):
        self.repo.git.checkout(self.original_branch)


@dataclass(frozen=True)
class UndoCreateHead(UndoCommand):
    repo: Repo
    branch_name: BranchName

    def undo(self):
        self.repo.git.branch("-D", self.branch_name)


@dataclass(frozen=True)
class UndoCreateNewBranch(UndoCommand):
    repo: Repo
    branch_name: BranchName

    def undo(self):
        try:
            self.repo.git.push("origin", "--delete", self.branch_name)
        except GitCommandError as e:
            if "remote ref does not exist" not in str(e):
                raise e
        self.repo.git.branch("-D", self.branch_name)


@dataclass(frozen=True)
class UndoCommitAndPushEverything(UndoCommand):
    repo: Repo

    def undo(self):
        self.repo.git.reset('HEAD^ --soft')
        self.repo.git.push("-f")


@dataclass(frozen=True)
class GitWrapper(GitWrapperAbstract):
    repo: Repo
    MOB_FILE_NAME: str = '.mob.json'

    def branch_exists(self, branch_name: BranchName) -> bool:
        return str(branch_name) in self.repo.branches or str(branch_name) in self.repo.remotes.origin.refs

    def checkout(self, branch_name: BranchName, fail_if_not_mob_branch: bool = True) -> UndoCommand:
        self.__fail_if_dirty()

        original_branch = BranchName(self.repo.active_branch.name or self.repo.active_branch.commit.hexsha)
        if original_branch == branch_name:
            try:
                if fail_if_not_mob_branch:
                    self.__fail_if_not_mob_branch()
                return UndoCommand.empty()
            except NotMobBranch as e:
                raise e

        self.repo.git.fetch('--all')
        self.repo.git.checkout(branch_name)

        undo_checkout = UndoCheckout(self.repo, original_branch)
        try:
            if fail_if_not_mob_branch:
                self.__fail_if_not_mob_branch()
        except NotMobBranch as e:
            undo_checkout()
            raise e
        return undo_checkout

    def create_new_mob_branch(self, branch_name: BranchName, mob_data: MobData) -> UndoCommand:
        self.__fail_if_dirty()

        undo_command = ComposedUndoCommand([])
        original_branch = self.__get_current_branch_name_or_sha_if_detached()

        self.repo.git.fetch('--all')
        self.repo.create_head(branch_name, f'origin/{self.__get_main_branch_name()}')
        undo_command = undo_command.with_command(UndoCreateHead(self.repo, branch_name))
        try:
            self.repo.git.checkout(branch_name)
            undo_command = undo_command.with_command(UndoCheckout(self.repo, original_branch))
            mob_data.save_to_file(self.__mob_file_path())
            undo_command = undo_command.with_command(self.__commit_and_push_everything("WIP mob: start session"))
        except Exception as e:
            undo_command.undo()
            raise e

        return undo_command

    def __get_current_branch_name_or_sha_if_detached(self) -> BranchName:
        return BranchName(self.repo.active_branch.name or self.repo.active_branch.commit.hexsha)

    def __is_dirty(self) -> bool:
        """
        Returns:
            True if the working directory is not clean, False otherwise
        """
        return bool(self.repo.is_dirty())

    def __get_mob_data(self) -> MobData | None:
        try:
            return MobData.from_file(self.__mob_file_path())
        except FileNotFoundError:
            return None

    def __is_mob_branch(self) -> bool:
        return self.__get_mob_data() is not None

    def __fail_if_not_mob_branch(self):
        if not self.__is_mob_branch():
            raise NotMobBranch.create()

    def __fail_if_dirty(self):
        if self.repo.is_dirty():
            raise WorkingDirectoryNotClean.create()

    def __mob_file_path(self):
        return f"{self.repo.working_dir}/{self.MOB_FILE_NAME}"

    def __get_main_branch_name(self) -> BranchName | None:
        all_possible_names = ['master', 'main']
        for branch in all_possible_names:
            if branch in self.repo.remotes.origin.refs:
                return BranchName(branch)

        return None

    def __commit_and_push_everything(self, message: str) -> UndoCommitAndPushEverything:
        self.__fail_if_not_mob_branch()

        self.repo.git.add('-A')
        self.repo.git.commit('-m', message)
        self.repo.git.push("origin", self.repo.active_branch.name, "--set-upstream")
        return UndoCommitAndPushEverything(self.repo)

    # def __create_local_branch_from_origin_main(self, new_branch: BranchName):
    #     self.repo.git.fetch('--all')
    #     self.repo.create_head(new_branch, f'origin/{self.get_main_branch_name()}')
    #     return UndoCreateHead(new_branch)
