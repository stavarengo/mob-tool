from dataclasses import dataclass

from git import Repo

from mob.GitCli.GitCliInterface import UndoCommand


@dataclass(frozen=True)
class UndoAddFileToGitInfoExclude(UndoCommand):
    repo: Repo
    new_entry: str

    def undo(self):
        file_path = f'{self.repo.git_dir}/info/exclude'
        try:
            with open(file_path, 'r') as f:
                entries = [entry for entry in f.readlines() if entry != self.new_entry]
                with open(file_path, 'w') as f:
                    f.write(''.join(entries))
        except FileNotFoundError:
            pass
