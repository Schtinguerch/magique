from typing import Callable, List, Any, Self


class NotifyUpdated:
    def __init__(self):
        self._observers: List[Callable[[Any], Any]] = []

    def raise_update_event(self) -> None:
        for observer_func in self._observers:
            observer_func(self)

    def attach_on_update(self, callback: Callable[[Any], Any]) -> None:
        self._observers.append(callback)

    def detach_on_update(self, callback: Callable[[Any], Any]) -> bool:
        if callback in self._observers:
            self._observers.remove(callback)
            return True
        return False

    def __add__(self, callback: Callable[[Any], Any]) -> Self:
        self.attach_on_update(callback)
        return self

    def __sub__(self, callback: Callable[[Any], Any]) -> Self:
        self.detach_on_update(callback)
        return self
