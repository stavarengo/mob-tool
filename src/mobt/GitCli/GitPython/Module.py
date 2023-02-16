import os

from git import Repo
from injector import Module as InjectorModule, singleton


class Module(InjectorModule):
    def configure(self, binder):
        binder.bind(Repo, to=Repo(os.getcwd(), search_parent_directories=True), scope=singleton)
