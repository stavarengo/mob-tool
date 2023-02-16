from dataclasses import dataclass

from injector import inject

from mobt.WorkDir import WorkDir


@inject
@dataclass(frozen=True)
class MobSecrets(str):
    work_dir: WorkDir

    def last_team_members_file_path(self):
        return f'{self.work_dir}/.mobt.last_team.json'

    def settings_file_path(self):
        return f'{self.work_dir}/.mobt.settings.json'
