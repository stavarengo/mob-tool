from injector import Injector


def configure(binder):
    # binder.bind(GitWrapperAbstract, to=GitWrapper, scope=singleton)
    pass


di = Injector([configure])
