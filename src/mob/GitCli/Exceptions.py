from mob.MobException import MobException


class WorkingDirectoryNotClean(MobException):
    @classmethod
    def create(cls):
        return cls("Work directory is not clean.")
