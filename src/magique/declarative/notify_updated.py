from typing import Callable, List, Any, Self, Dict


Handler = Callable[[Any], Any]


class NotifyUpdated:
    """
    The root class for observable objects able to notify its updates

    Provides two types of updates:
        1. Object update, object just has been updated
        2. Object property has been updated, certain property update by its name

    classes from `magique.declarative` are inherited from the ``NotifyUpdated`` class,
    and have the same notify and update tools, functions and compatible
    """

    def __init__(self):
        self._observers: List[Handler] = []
        self._property_observers: Dict[str, Self] = {}
        self._property_receivers: Dict[str, Self] = {}
        self._property_two_way_listeners: Dict[str, Self] = {}

        if not hasattr(self, "value"):
            self.value: Any = None

        self.is_sending: bool = False

    def __repr__(self) -> str:
        return f"<NotifyUpdated: observers_len={len(self._observers)}, value={self.value}>"

    def property_updated(self, property_name: str) -> Self:
        """
        Listening the specified property values updates by its name
        :param property_name: ``str`` name of specified property
        :return: New ``NotifyUpdated`` instance calling ``raise_update_event()`` when only the property changed
        """

        if property_name in self._property_observers:
            return self._property_observers[property_name]

        notify_prop_updated = NotifyUpdated()
        notify_prop_updated.value = getattr(self, property_name)
        self._property_observers[property_name] = notify_prop_updated
        return notify_prop_updated

    def property_received(self, property_name: str) -> Self:
        """
        Creates an ``ObservableReceiver`` for the specified property by its name
        :param property_name: ``str`` name of specified property
        :return: new ``ObservableReceiver`` updating property's value when receiver's ``value`` is updated
        """

        from .observable_receiver import ObservableReceiver

        if property_name in self._property_receivers:
            return self._property_receivers[property_name]

        receiver = ObservableReceiver(lambda v: setattr(self, property_name, v), getattr(self, property_name))
        self._property_receivers[property_name] = receiver
        return receiver

    def property(self, property_name: str) -> Self:
        """
        It's a two-way property listener. Allows catch updates of property updates and updating
        property when its receiver got new value

        Contains property's ``property_updated()`` and ``property_received()`` instances
        by its name

        :param property_name: property_name: ``str`` name of specified property
        :return: new ``PropertyListener`` instance for two-way property listening
        """

        from .property_listener import PropertyListener

        if property_name in self._property_two_way_listeners:
            return self._property_two_way_listeners[property_name]

        # noinspection PyTypeChecker
        listener = PropertyListener(self.property_updated(property_name), self.property_received(property_name))
        self._property_two_way_listeners[property_name] = listener
        return listener

    def properties_updated(self, *property_names: str) -> List[Self]:
        """
        Allows start listening by multiple properties in single
        method invoke
        :param property_names: collection of ``str`` property names
        :return: new ``List`` of ``NotifyUpdated`` instances calling
        ``raise_update_event()`` when property by its name has been changed
        """

        return [self.property_updated(name) for name in property_names]

    def properties_received(self, *property_names: str) -> List[Self]:
        """
        Creates multiple ``ObservableReceiver`` instances for the specified properties
        by its name. Its updates, triggers specified properties updates

        :param property_names: collection of ``str`` property names
        :return: new ``List`` of ``ObservableReceiver`` updating property's
        value when receiver's ``value`` is updated
        """

        return [self.property_received(name) for name in property_names]

    def properties(self, *property_names: str) -> List[Self]:
        """
        Creates multiple ``PropertyListener`` instances in a single method. Every instance
        is a two-way property listener containing property's ``property_updated()``
        and ``property_received()`` instances by its name

        :param property_names: collection of ``str`` property names
        :return: new ``List`` of ``PropertyListener`` instances for two-way property listening
        """

    def raise_update_event(self) -> None:
        """
        Raises the whole object update event, invoking subscribed functions.
        Supports to be invoked manually
        """

        for observer_func in self._observers:
            observer_func(self)

    def raise_property_update(self, property_name: str) -> None:
        """
        Raises the property update by its name, invoking subscribed functions
        to ``property_updated`` functions. After the raise, general
        ``raise_update_event()`` invokes

        :param property_name: property name which event to be raised
        """

        if property_name not in self._property_observers: return

        notify_prop_updated: Self = self._property_observers[property_name]
        notify_prop_updated.raise_update_event()

    def raise_update_if_values_diff(self, a: Any, b: Any) -> bool:
        """
        Raises the whole object update event, invoking subscribed functions
        if passed values are different (a != b)
        Supports to be invoked manually

        :param a: an old value
        :param b: a new value, to be compared with the old value
        :return: are passed value different (a != b)
        """

        are_same: bool = a == b
        if are_same:
            return False

        self.raise_update_event()
        return True

    def raise_property_update_if_values_diff(self, property_name: str, a: Any, b: Any) -> bool:
        """
        Raises the property update by its name, invoking subscribed functions
        to ``property_updated`` functions if passed parameters are different (a != b).
        After the raise, general ``raise_update_event`` invokes

        :param property_name: property name which event to be raised
        :param a: an old property value
        :param b: a new property value, to be compared with the old value
        """

        if property_name not in self._property_observers:
            return False

        notify_prop_updated: Self = self._property_observers[property_name]
        notify_prop_updated.value = b
        if notify_prop_updated.raise_update_if_values_diff(a, b):
            self.raise_update_event()
            return True

        return False

    def attach_on_update(self, callback: Handler) -> None:
        """
        Subscribes specified function to the ``raise_update_event()``.
        If object instance is updated, your function will be invoked

        :param callback: a function to be subscribed to an update event
        """

        self._observers.append(callback)

    def detach_on_update(self, callback: Handler) -> bool:
        """
        Unsubscribes specified function from the ``raise_update_event()``.
        If object instance is updated, your function will not be invoked though

        :param callback: a function is being subscribed to an update event,
        to be unsubscribed

        Also, alternative C#-like syntax is supported, through
        ``some_obj += callback``
        """

        if callback in self._observers:
            self._observers.remove(callback)
            return True
        return False

    def detach_all_handlers(self) -> None:
        """
        Unsubscribes all functions which are subscribed to current
        object instance for update event

        Also, alternative C#-like syntax is supported, through
        ``some_obj -= callback``
        """

        self._observers.clear()

    def __add__(self, callback: Handler) -> Self:
        self.attach_on_update(callback)
        return self

    def __sub__(self, callback: Handler) -> Self:
        self.detach_on_update(callback)
        return self


def notify_property_updated(
        get_value_function: Callable[[NotifyUpdated], Any],
        property_name: str | None = None) -> Callable:
    """
    Decorator for class methods (NotifyUpdated and its child classes), allows
    automatically notify if property is updated, invoking
    ``raise_property_update_if_values_diff()``

    :param get_value_function: invoke value getter, to check the value before
    :param property_name: change updating property name, if method name doesn't same to property name
    and after decorated method invokation
    """

    def decorator(target_function: Callable) -> Callable:
        final_property_name: str = property_name or target_function.__name__

        def wrapper(self, *args, **kwargs):
            old_value: Any = get_value_function(self)
            target_function(self, *args, **kwargs)

            new_value: Any = get_value_function(self)
            self.raise_property_update_if_values_diff(final_property_name, old_value, new_value)
        return wrapper
    return decorator
