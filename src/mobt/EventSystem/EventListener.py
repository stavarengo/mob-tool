from abc import ABC, abstractmethod
from dataclasses import dataclass

from mobt.EventSystem.EventBase import EventBase


@dataclass(frozen=True)
class EventListener(ABC):

    @abstractmethod
    def handle(self, event: EventBase) -> None:
        pass

    def __call__(self, event: EventBase):
        self.handle(event)
