from .notify_updated import NotifyUpdated
from typing import Callable, List, TypeVar, Generic, Any


T = TypeVar('T')


class Observable(Generic[T], NotifyUpdated):
    def __init__(self, initial_value: T | None = None):
        super().__init__()
        self._value = initial_value
        self._observers: List[Callable[[T], Any]] = []

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, new_value: T):
        if new_value == self._value:
            return

        self._value = new_value
        self.raise_update_event()

    def no_event_set_value(self, new_value: T):
        self._value = new_value

    def attach_on_update(self, callback: Callable[[T], Any]) -> None:
        self._observers.append(callback)

    def detach_on_update(self, callback: Callable[[T], Any]) -> bool:
        if callback in self._observers:
            self._observers.remove(callback)
            return True
        return False

    def raise_update_event(self) -> None:
        for observer_func in self._observers:
            observer_func(self._value)


def obs(initial_value: T) -> Observable[T]:
    return Observable(initial_value)
