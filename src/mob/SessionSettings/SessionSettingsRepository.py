from dataclasses import dataclass
from typing import Union

from injector import inject

from mob.FileAccess.FileAccess import FileAccess
from mob.MobSecrets import MobSecrets
from mob.SessionSettings.SessionSettings import SessionSettings


@inject
@dataclass
class SessionSettingsRepository:
    secrets: MobSecrets
    file: FileAccess

    def find(self) -> Union[SessionSettings, None]:
        content = self.file.read(self.secrets.settings_file_path())
        return content and SessionSettings.schema().loads(content) or None

    def save(self, members: SessionSettings) -> None:
        self.file.save(SessionSettings.schema().dumps(members, indent=2), self.secrets.settings_file_path())

    def delete(self) -> None:
        self.file.delete(self.secrets.settings_file_path())
