from dataclasses import dataclass

from git import Repo

from mob.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass(frozen=False)
class _PushUndoContext:
    unset_upstream: bool = False
    delete_remote_branch: bool = False
    remote_branch_original_hash: str = None


@dataclass()
class AddEntryToInfoExclude(GitAction):
    repo: Repo
    new_entry: str

    def _execute(self) -> None:
        file_path = f'{self.repo.git_dir}/info/exclude'
        try:
            with open(file_path, 'r') as f:
                entries = f.readlines()
        except FileNotFoundError:
            entries = []

        new_entry = self.__sanitize_entry(self.new_entry)
        if new_entry not in entries:
            with open(file_path, 'w') as f:
                entries.append(new_entry)
                f.write(''.join(entries))

    def _undo(self):
        file_path = f'{self.repo.git_dir}/info/exclude'
        new_entry = self.__sanitize_entry(self.new_entry)

        try:
            with open(file_path, 'r') as f:
                entries = [entry for entry in f.readlines() if entry != new_entry]
                with open(file_path, 'w') as f:
                    f.write(''.join(entries))
        except FileNotFoundError:
            pass

    def __sanitize_entry(self, entry: str) -> str:
        return f"{entry.replace(self.repo.working_dir, '')}\n"
