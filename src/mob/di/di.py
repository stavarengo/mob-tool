from injector import Injector

from mob.GitCli.Module import Module as GitCliModule
from mob.Module import Module as MobModule

di = Injector([MobModule, GitCliModule])
di.binder.bind(Injector, to=di)
