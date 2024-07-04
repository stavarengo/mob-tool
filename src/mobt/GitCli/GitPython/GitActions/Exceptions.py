from mobt.MobException import MobException


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

class StashNameAreadyExists(MobException):
    @classmethod
    def create(cls, stash_name: str) -> 'StashNameAreadyExists':
        return cls(f"Stash with name '{stash_name}' already exists.")

class StashNameNotFound(MobException):
    @classmethod
    def create(cls, stash_name: str) -> 'StashNameNotFound':
        return cls(f"Stash with name '{stash_name}' not found.")