class ActionAlreadyExecuted(Exception):
    @classmethod
    def create(cls, action: str) -> 'ActionAlreadyExecuted':
        return cls(f"Action {action} already executed")


class ActionAlreadyUndo(Exception):
    @classmethod
    def create(cls, action: str) -> 'ActionAlreadyUndo':
        return cls(f"Action {action} already undo")
