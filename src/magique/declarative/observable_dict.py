from typing import TypeVar, Generic, Dict
from .observable import Observable


K = TypeVar("K")
V = TypeVar("V")


class ObservableDict(Observable, Generic[K, V]):
    def __init__(self, initial_dict: Dict | None = None):
        self._target_dict = initial_dict or {}
        super().__init__(initial_value=self._target_dict)

    def __setitem__(self, key: K, value: V):
        self._value[key] = value
        self.raise_update_event()

    def __delitem__(self, key: K):
        del self._value[key]
        self.raise_update_event()

    def clear(self):
        self._value.clear()
        self.raise_update_event()

    def update(self, *args, **kwargs):
        self._value.update(*args, **kwargs)
        self.raise_update_event()

    def __getitem__(self, key: K) -> V:
        return self._value[key]

    def __len__(self) -> int:
        return len(self._value)

    def __repr__(self) -> str:
        return repr(self._value)
