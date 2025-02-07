from typing import Any, TypeVar, Callable
from .observable import Observable


T = TypeVar('T')


class ObservableReceiver(Observable[T]):
    """
    A container inherited from ``Observable`` with the ``value``
    property, which invokes a special ``setter_function``
    when the property is updated by new different value

    Allows update non-observable data when Observable variable
    is updated
    """

    def __init__(self, setter_function: Callable[[Any], Any], initial_value: T | None = None):
        super().__init__(initial_value)
        self.setter_function = setter_function

    @Observable.value.setter
    def value(self, new_value: T):
        self.setter_function(new_value)
        if new_value == self._value:
            return

        self._value = new_value
        self.raise_update_event()
