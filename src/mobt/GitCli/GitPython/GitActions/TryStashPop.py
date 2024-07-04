from dataclasses import dataclass

from git import Repo

from mobt import echo
from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.GitPython.GitActions.Exceptions import StashNameAreadyExists
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction
from mobt.GitCli.GitPython.GitActions.GitActionWasExecuted import GitActionWasExecuted
from mobt.GitCli.GitPython.GitActions.shared.find_stash_index_by_name import find_stash_index_by_name


@dataclass()
class TryStashPop(GitAction):
    repo: Repo
    stash_name: str
    event_manager: EventManager

    def _execute(self) -> None:
        stash_index = find_stash_index_by_name(self.repo, self.stash_name)
        if stash_index is None:
            raise StashNameAreadyExists.create(self.stash_name)
        try:
            self.repo.git.stash('pop', f'stash@{{{stash_index}}}')
        except BaseException as e:
            echo(
                f"CONFLICT detected! {e}",
                fg='bright_red'
            )
            self.repo.git.reset('--hard')
            self.repo.git.clean('-f', '-d')

            echo(
                f"CONFLICT detected!",
                fg='bright_red'
            )
            echo(
                f"Couldn't pop stash due to conflicts.",
                fg='bright_red'
            )
            echo(
                f"Use the command below to pop your stash and resolve the conflicts manually.",
                fg='bright_yellow'
            )
            echo(
                f"git stash pop stash@{{{stash_index}}}",
                fg='bright_yellow'
            )

    def _undo(self) -> None:
        pass
