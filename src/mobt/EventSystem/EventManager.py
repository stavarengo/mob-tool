from dataclasses import dataclass
from typing import Callable, Type, Union

from mobt.EventSystem.EventBase import EventBase
from mobt.EventSystem.EventListener import EventListener

_Listener = Union[EventListener, Callable[[Type[EventBase]], None]]


@dataclass()
class EventManager:
    def __init__(self):
        self._listeners = {}

    def add_listener(self, event: Type[EventBase], listener: _Listener) -> Callable[[], None]:
        """
        Add a listener for an event.
        :param event:
        :param listener:
        :return: A function that removes the listener.
        """
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(listener)
        return lambda: self.remove_listener(event, listener)

    def remove_listener(self, event: Type[EventBase], listener: _Listener) -> None:
        if event in self._listeners:
            if listener in self._listeners[event]:
                self._listeners[event].remove(listener)
            if not self._listeners[event]:
                del self._listeners[event]

    def dispatch_event(self, event: EventBase) -> None:
        event_class = event.__class__
        if event_class in self._listeners:
            for listener in self._listeners[event_class]:
                listener(event)
