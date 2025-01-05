from typing import List, TypeVar, Generic
from .observable import Observable


T = TypeVar('T')


class ObservableList(Observable[List], Generic[T]):
    def __init__(self, initial_list: List[T] | None = None):
        self._target_list: List[T] = initial_list or []
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

    def __len__(self):
        return len(self._value)

    def __repr__(self):
        return repr(self._value)
