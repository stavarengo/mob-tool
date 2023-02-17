from injector import Binder, CallableProvider, Module as InjectorModule


class Module(InjectorModule):

    def configure(self, binder: Binder):
        from mobt.WorkDir import WorkDir
        def _provideWorkDir() -> WorkDir:
            from git import Repo
            return WorkDir(binder.injector.get(Repo).working_dir)

        binder.bind(WorkDir, to=CallableProvider(_provideWorkDir))
