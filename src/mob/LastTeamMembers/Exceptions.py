from mob.MobException import MobException


class MemberNameCanNotBeEmpty(MobException):
    @staticmethod
    def create() -> 'MemberNameCanNotBeEmpty':
        return MemberNameCanNotBeEmpty("Member name cannot be empty.")


class YouCantMobWithLessThanTwoMembers(MobException):
    @staticmethod
    def create() -> 'YouCantMobWithLessThanTwoMembers':
        return YouCantMobWithLessThanTwoMembers("You can't mob with less than two members.")


class ThereAreDuplicatedTeamMembers(MobException):
    @staticmethod
    def create() -> 'ThereAreDuplicatedTeamMembers':
        return ThereAreDuplicatedTeamMembers("There are duplicated team members.")
