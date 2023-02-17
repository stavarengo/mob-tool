from injector import Module as InjectorModule, singleton


class Module(InjectorModule):
    def configure(self, binder):
        from mobt.GitCli.GitCliInterface import GitCliInterface
        from mobt.GitCli.GitPython.GitCliWithGitPython import GitCliWithGitPython
        from mobt.GitCli.GitPython.Module import Module as GitPythonModule

        binder.install(GitPythonModule)
        binder.bind(GitCliInterface, to=GitCliWithGitPython, scope=singleton)
