from injector import Injector

from mobt.GitCli.Module import Module as GitCliModule
from mobt.JsonSerializer.Module import Module as JsonSerializerModule
from mobt.Module import Module as MobModule

di = Injector([MobModule, GitCliModule, JsonSerializerModule])
di.binder.bind(Injector, to=di)
