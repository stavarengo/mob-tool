from injector import Module as InjectorModule, singleton

from mobt.GitCli.GitCliInterface import GitCliInterface
from mobt.GitCli.GitPython.GitCliWithGitPython import GitCliWithGitPython
from mobt.GitCli.GitPython.Module import Module as GitPythonModule


class Module(InjectorModule):
    def configure(self, binder):
        binder.install(GitPythonModule)
        binder.bind(GitCliInterface, to=GitCliWithGitPython, scope=singleton)
