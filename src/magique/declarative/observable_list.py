from typing import Any, List, TypeVar, Generic, Iterable, Iterator, Callable
from .observable import Observable


T = TypeVar('T')


class ObservableList(Observable[List], Generic[T]):
    """
    It's a standard ``List``, but every mutation operation
    invokes ``raise_update_event()`` with its subscribed
    functions, supports all basic list operations

    If no argument is given, the constructor creates a new empty list.
    The argument must be an iterable if specified
    """

    def __init__(self, initial_iterable: Iterable[T] | None = None):
        if initial_iterable is None:
            self._initializer_list = []
        elif isinstance(initial_iterable, list):
            self._initializer_list = initial_iterable
        else:
            self._initializer_list = list(initial_iterable)

        super().__init__(initial_value=self._initializer_list)

    def append(self, item: T):
        """ Appends object to the end of the list """

        self._value.append(item)
        self.raise_update_event()

    def remove(self, item: T):
        """
        Removes first occurrence of value

        Raises ``ValueError`` if the value is not present
        """

        self._value.remove(item)
        self.raise_update_event()

    def remove_many(self, items: Iterable[T]):
        """
        Performs multiply ``remove()`` operations, but with
        single ``raise_update_event``, because it's recognized
        as single operation
        """

        for item in items:
            self._value.remove(item)

        self.raise_update_event()

    def clear(self):
        """ Removes all items from list """

        self._value.clear()
        self.raise_update_event()

    def extend(self, items: Iterable[T]):
        """ Extends list by appending elements from the iterable """

        self._value.extend(items)
        self.raise_update_event()

    def __getitem__(self, index):
        value: T = self._value[index]
        return ObservableList(value) if isinstance(value, list) else value

    def __setitem__(self, index, value):
        self._value[index] = value
        self.raise_update_event()

    def __delitem__(self, index):
        del self._value[index]
        self.raise_update_event()

    def __contains__(self, item: Any) -> bool:
        return item in self._value

    def __iter__(self) -> Iterator[T]:
        return self._value.__iter__()

    def __len__(self):
        return len(self._value)

    def __repr__(self):
        return repr(self._value)


def ol(initial_iterable: Iterable[T] | None = None) -> ObservableList[T]:
    """
    Creates a new instance of ``ObservableList`` from any ``Iterable`` object
    """

    return ObservableList(initial_iterable)


olist: Callable[[Iterable[T]], ObservableList[T]] = ol
