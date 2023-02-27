from injector import Module as InjectorModule, singleton


class Module(InjectorModule):
    def configure(self, binder):
        from mobt.EventSystem.EventManager import EventManager

        binder.bind(EventManager, to=EventManager, scope=singleton)
