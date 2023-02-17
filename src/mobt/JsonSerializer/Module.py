from injector import Module as InjectorModule, singleton


class Module(InjectorModule):
    def configure(self, binder):
        from mobt.JsonSerializer.DataClassesSerializer import DataClassesSerializer
        from mobt.JsonSerializer.JsonSerializerInterface import JsonSerializerInterface

        binder.bind(JsonSerializerInterface, to=DataClassesSerializer, scope=singleton)
