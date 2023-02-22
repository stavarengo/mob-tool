from mobt.MobException import MobException


class SessionSettingsAlreadyExists(MobException):
    @staticmethod
    def create() -> 'SessionSettingsAlreadyExists':
        return SessionSettingsAlreadyExists('Can not create another session settings.')


class SessionSettingsNotFound(MobException):
    @staticmethod
    def create() -> 'SessionSettingsNotFound':
        return SessionSettingsNotFound('Session settings not found. This is probably not a mob branch.')


class TeamsCanNotHaveLessThaTwoMembers(MobException):
    @staticmethod
    def create() -> 'TeamsCanNotHaveLessThaTwoMembers':
        return TeamsCanNotHaveLessThaTwoMembers('Teams can not have less than two members.')

    def extra_help(self) -> str:
        return "Try again with the parameter `-m` to set your team members."
