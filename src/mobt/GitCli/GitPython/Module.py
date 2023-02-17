from injector import Module as InjectorModule, singleton


class Module(InjectorModule):
    def configure(self, binder):
        from git import Repo
        import os

        binder.bind(Repo, to=Repo(os.getcwd(), search_parent_directories=True), scope=singleton)
