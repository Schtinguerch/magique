from typing import List, TypeVar, Generic, Iterable, Callable
from .observable import Observable


T = TypeVar('T')


class ObservableList(Observable[List], Generic[T]):
    def __init__(self, initial_iterable: Iterable[T] | None = None):
        if initial_iterable is None:
            self._target_list = []
        elif isinstance(initial_iterable, list):
            self._target_list = initial_iterable
        else:
            self._target_list = list(initial_iterable)

        super().__init__(initial_value=self._target_list)

    def append(self, item: T):
        self._value.append(item)
        self.raise_update_event()

    def remove(self, item: T):
        self._value.remove(item)
        self.raise_update_event()

    def clear(self):
        self._value.clear()
        self.raise_update_event()

    def extend(self, items: List[T]):
        self._value.extend(items)
        self.raise_update_event()

    def __getitem__(self, index):
        value = self._value[index]
        return ObservableList(value) if isinstance(value, list) else value

    def __setitem__(self, index, value):
        self._value[index] = value
        self.raise_update_event()

    def __delitem__(self, index):
        del self._value[index]
        self.raise_update_event()

    def __len__(self):
        return len(self._value)

    def __repr__(self):
        return repr(self._value)


def ol(initial_iterable: Iterable[T] | None = None) -> ObservableList[T]:
    return ObservableList(initial_iterable)


olist: Callable[[Iterable[T]], ObservableList[T]] = ol
