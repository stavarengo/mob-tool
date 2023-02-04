from mob.MobException import MobException


class SessionSettingsAlreadyExists(MobException):
    @staticmethod
    def create() -> 'SessionSettingsAlreadyExists':
        return SessionSettingsAlreadyExists('Can not create another session settings.')
