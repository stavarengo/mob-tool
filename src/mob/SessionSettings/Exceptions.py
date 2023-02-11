from mob.MobException import MobException


class SessionSettingsAlreadyExists(MobException):
    @staticmethod
    def create() -> 'SessionSettingsAlreadyExists':
        return SessionSettingsAlreadyExists('Can not create another session settings.')


class SessionSettingsNotFound(MobException):
    @staticmethod
    def create() -> 'SessionSettingsNotFound':
        return SessionSettingsNotFound('Session settings not found. This is probably not a mob branch.')
