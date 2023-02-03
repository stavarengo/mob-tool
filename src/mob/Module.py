from git import Repo
from injector import CallableProvider, Injector, Module as InjectorModule, inject

from mob.WorkDir import WorkDir


class Module(InjectorModule):
    @inject
    def __provideWorkDir(self, injector: Injector) -> WorkDir:
        return WorkDir(injector.get(Repo).working_dir)

    def configure(self, binder):
        binder.bind(WorkDir, to=CallableProvider(self.__provideWorkDir))
