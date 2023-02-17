from injector import Module as InjectorModule, singleton


class Module(InjectorModule):
    def configure(self, binder):
        from mobt.Cache.CacheInterface import CacheInterface
        from mobt.Cache.FileSystemCache import FileSystemCache
        binder.bind(CacheInterface, to=FileSystemCache, scope=singleton)
