from injector import Module as InjectorModule, singleton

from mob.JsonSerializer.DataClassesSerializer import DataClassesSerializer
from mob.JsonSerializer.JsonSerializerInterface import JsonSerializerInterface


class Module(InjectorModule):
    def configure(self, binder):
        binder.bind(JsonSerializerInterface, to=DataClassesSerializer, scope=singleton)
