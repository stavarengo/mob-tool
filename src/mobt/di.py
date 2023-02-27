from injector import Injector

from mobt.Cache.Module import Module as CacheModule
from mobt.EventSystem.Module import Module as EventSystemModule
from mobt.GitCli.Module import Module as GitCliModule
from mobt.JsonSerializer.Module import Module as JsonSerializerModule
from mobt.Module import Module as MobModule

di = Injector([MobModule, GitCliModule, JsonSerializerModule, CacheModule, EventSystemModule])
di.binder.bind(Injector, to=di)
