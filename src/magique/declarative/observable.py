from .notify_updated import NotifyUpdated
from typing import Callable, List, TypeVar, Generic, Any


T = TypeVar('T')


class Observable(Generic[T], NotifyUpdated):
    """
    A container inherited from ``NotifyUpdated`` with the ``value``
    property, which  invoked ``raise_update_event()`` when the
    ``value`` property is updated by new different value
    """

    def __init__(self, initial_value: T | None = None):
        super().__init__()
        self._value = initial_value
        self._observers: List[Callable[[T], Any]] = []

    def __str__(self) -> str:
        return f"obs({self._value.__str__()})"

    def __repr__(self) -> str:
        return f"<obs: value={self._value.__repr__()}; observers_len={len(self._observers)}>"

    def __lshift__(self, other: T):
        self.value = other

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
        """
        The way to update Observable's value without
        ``raise_update_event()`` invokation
        """

        self._value = new_value

    def raise_update_event(self) -> None:
        """
        Raises the whole object update event, invoking subscribed functions.
        Supports to be invoked manually

        The containing ``value`` is passed to every invoked handler, instead
        of the class instance like ``NotifyUpdated`` instances
        """

        for observer_func in self._observers:
            observer_func(self._value)


def obs(initial_value: T | None = None) -> Observable[T]:
    """
    Creates a new instance of ``Observable[T]`` object
    :param initial_value: start value to be stored
    """

    return Observable(initial_value)
