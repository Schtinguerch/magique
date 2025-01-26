from typing import TypeVar, Generic, Dict, Callable, Iterable, Any
from .observable import Observable


K = TypeVar("K")
V = TypeVar("V")


class ObservableDict(Observable[Dict], Generic[K, V]):
    """
    It's a standard ``Dict``, but every mutation operation
    invokes ``raise_update_event()`` with its subscribed
    functions, supports all basic list operations

    If no argument is given, the constructor creates a new empty dict.
    The argument must be an iterable if specified
    """

    def __init__(self, initial_dict: Dict | Iterable | zip | None = None, **kwargs: Dict[Any, Any]):
        if initial_dict is None:
            self._target_dict = {}
        elif isinstance(initial_dict, zip):
            self._target_dict = dict(initial_dict)
        elif isinstance(initial_dict, Iterable):
            self._target_dict = dict(initial_dict)
        else:
            self._target_dict = initial_dict

        self._target_dict.update(kwargs)
        super().__init__(initial_value=self._target_dict)

    def __setitem__(self, key: K, value: V):
        self._value[key] = value
        self.raise_update_event()

    def __delitem__(self, key: K):
        del self._value[key]
        self.raise_update_event()

    def clear(self):
        """ Remove all items from the dictionary """

        self._value.clear()
        self.raise_update_event()

    def update(self, *args, **kwargs):
        """ Adds new key-value pairs, or changes existing """

        self._value.update(*args, **kwargs)
        self.raise_update_event()

    def __getitem__(self, key: K) -> V:
        return self._value[key]

    def __len__(self) -> int:
        return len(self._value)

    def __repr__(self) -> str:
        return repr(self._value)


def od(initial_dict: Dict | zip | Iterable | None = None) -> ObservableDict:
    """
    Creates a new instance of ``ObservableDict`` from another dictionary,
    or zip object, or another iterable[key, value]
    """

    return ObservableDict(initial_dict)


odict: Callable[[Dict | zip | None], ObservableDict] = od
