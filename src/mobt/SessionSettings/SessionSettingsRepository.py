from dataclasses import dataclass
from typing import Union

from injector import inject

from mobt.FileAccess.FileAccess import FileAccess
from mobt.JsonSerializer.JsonSerializerInterface import JsonSerializerInterface
from mobt.MobSecrets import MobSecrets
from mobt.SessionSettings.SessionSettings import SessionSettings


@inject
@dataclass
class SessionSettingsRepository:
    secrets: MobSecrets
    file: FileAccess
    serializer: JsonSerializerInterface

    def find(self) -> Union[SessionSettings, None]:
        content = self.file.read(self.secrets.settings_file_path())
        return content and self.serializer.from_json(SessionSettings, content) or None

    def save(self, members: SessionSettings) -> None:
        self.file.save(self.serializer.to_json(members), self.secrets.settings_file_path())

    def delete(self) -> None:
        self.file.delete(self.secrets.settings_file_path())
