from injector import Injector, singleton

from mob.GitWrapper.GitWrapper import GitWrapper
from mob.GitWrapper.GitWrapperAbstract import GitWrapperAbstract


def configure(binder):
    binder.bind(GitWrapperAbstract, to=GitWrapper, scope=singleton)


di = Injector([configure])
