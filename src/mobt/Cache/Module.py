from injector import Module as InjectorModule, singleton

from mobt.Cache.CacheInterface import CacheInterface
from mobt.Cache.FileSystemCache import FileSystemCache


class Module(InjectorModule):
    def configure(self, binder):
        binder.bind(CacheInterface, to=FileSystemCache, scope=singleton)
