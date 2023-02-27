from dataclasses import dataclass

from mobt.EventSystem.EventBase import EventBase


@dataclass(frozen=True)
class MobAppRelevantOperationHappened(EventBase):
    human_log: str

    def __post_init__(self):
        assert self.human_log, "human_log must not be empty"
