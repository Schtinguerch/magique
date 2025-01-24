from typing import Callable, List, Any, Self, Dict


Handler = Callable[[Any], Any]


class NotifyUpdated:
    def __init__(self):
        self._observers: List[Handler] = []
        self._property_observers: Dict[str, Self] = {}

    def property_updated(self, property_name: str) -> Self:
        """
        Listening the specified property
        :param property_name: ``str`` name of specified property
        :return: ``NotifyUpdated`` instance calling ``raise_update_event()`` when only the property changed
        """

        if property_name in self._property_observers:
            return self._property_observers[property_name]

        notify_prop_updated = NotifyUpdated()
        self._property_observers[property_name] = notify_prop_updated
        return notify_prop_updated

    def raise_update_event(self) -> None:
        for observer_func in self._observers:
            observer_func(self)

    def raise_property_update(self, property_name: str) -> None:
        if property_name not in self._property_observers: return

        notify_prop_updated: Self = self._property_observers[property_name]
        notify_prop_updated.raise_update_event()

    def raise_update_if_values_diff(self, a: Any, b: Any) -> bool:
        are_same: bool = a == b
        if are_same:
            return False

        self.raise_update_event()
        return True

    def raise_property_update_if_values_diff(self, property_name: str, a: Any, b: Any) -> bool:
        if property_name not in self._property_observers:
            return False

        notify_prop_updated: Self = self._property_observers[property_name]
        if notify_prop_updated.raise_update_if_values_diff(a, b):
            self.raise_update_event()
            return True

        return False

    def attach_on_update(self, callback: Handler) -> None:
        self._observers.append(callback)

    def detach_on_update(self, callback: Handler) -> bool:
        if callback in self._observers:
            self._observers.remove(callback)
            return True
        return False

    def detach_all_handlers(self) -> None:
        self._observers.clear()

    def __add__(self, callback: Handler) -> Self:
        self.attach_on_update(callback)
        return self

    def __sub__(self, callback: Handler) -> Self:
        self.detach_on_update(callback)
        return self


def notify_property_updated(get_value_function: Callable[[NotifyUpdated], Any]) -> Callable:
    def decorator(target_function: Callable) -> Callable:
        def wrapper(self, *args, **kwargs):
            property_name: str = target_function.__name__

            old_value: Any = get_value_function(self)
            target_function(self, *args, **kwargs)

            new_value: Any = get_value_function(self)
            self.raise_property_update_if_values_diff(property_name, old_value, new_value)
        return wrapper
    return decorator
