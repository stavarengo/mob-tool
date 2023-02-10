from injector import Injector

from mob.GitCli.Module import Module as GitCliModule
from mob.JsonSerializer.Module import Module as JsonSerializerModule
from mob.Module import Module as MobModule

di = Injector([MobModule, GitCliModule, JsonSerializerModule])
di.binder.bind(Injector, to=di)
