from injector import Module as InjectorModule, singleton

from mob.GitCli.GitCliInterface import GitCliInterface
from mob.GitCli.GitPython.GitCliWithGitPython import GitCliWithGitPython
from mob.GitCli.GitPython.Module import Module as GitPythonModule


class Module(InjectorModule):
    def configure(self, binder):
        binder.install(GitPythonModule)
        binder.bind(GitCliInterface, to=GitCliWithGitPython, scope=singleton)
