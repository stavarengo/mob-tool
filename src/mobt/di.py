from injector import Injector

from mobt.Cache.Module import Module as CacheModule
from mobt.GitCli.Module import Module as GitCliModule
from mobt.JsonSerializer.Module import Module as JsonSerializerModule
from mobt.Module import Module as MobModule

di = Injector([MobModule, GitCliModule, JsonSerializerModule, CacheModule])
di.binder.bind(Injector, to=di)
