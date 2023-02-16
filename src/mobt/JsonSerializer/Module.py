from injector import Module as InjectorModule, singleton

from mobt.JsonSerializer.DataClassesSerializer import DataClassesSerializer
from mobt.JsonSerializer.JsonSerializerInterface import JsonSerializerInterface


class Module(InjectorModule):
    def configure(self, binder):
        binder.bind(JsonSerializerInterface, to=DataClassesSerializer, scope=singleton)
