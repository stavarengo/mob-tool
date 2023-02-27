from dataclasses import dataclass
from typing import Type

from mobt.EventSystem.EventBase import EventBase
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass(frozen=True)
class GitActionWasExecuted(EventBase):
    action: Type[GitAction]
    human_log: str

    def __post_init__(self):
        assert self.action, "action must not be empty"
        assert self.human_log, "human_log must not be empty"
