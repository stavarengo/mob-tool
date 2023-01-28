from injector import Injector, singleton

from mob.git_wrapper.git_wrapper import GitWrapper
from mob.git_wrapper.git_wrapper_abstract import GitWrapperAbstract


def configure(binder):
    binder.bind(GitWrapperAbstract, to=GitWrapper, scope=singleton)


di = Injector([configure])
