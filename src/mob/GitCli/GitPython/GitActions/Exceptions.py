from mob.MobException import MobException


class ActionAlreadyExecuted(MobException):
    @classmethod
    def create(cls, action: str) -> 'ActionAlreadyExecuted':
        return cls(f"Action {action} already executed")


class ActionAlreadyUndo(MobException):
    @classmethod
    def create(cls, action: str) -> 'ActionAlreadyUndo':
        return cls(f"Action {action} already undo")


class NonFastForwardPush(MobException):
    @classmethod
    def create(cls) -> 'NonFastForwardPush':
        return cls("Failed to push: non-fast-forward")
