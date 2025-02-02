from typing import List, Callable, Any, Iterable
from .notify_updated import NotifyUpdated


class WhenCondition:
    """
    The class responsible for catching ``NotifyUpdated`` events
    to start specified condition checking

    If conditions satisfied, specified functions are invoked
        1. ``observables`` - the collection of ``NotifyUpdated`` which updates are triggers to start conditions checking
        2. ``conditions`` - the collection of ``func() -> bool`` with some checks, True = condition is satisfied
        3. ``handlers`` - the collection of ``func()`` with some behavior if conditions are satisfied
        4. ``all_conditions_to_be_true`` True - need all conditions return True, False - at least one returns True
        5. ``max_activation_count`` - max count of ``handlers`` invokation if conditions are satisfied
    """

    def __init__(
            self,
            observables: Iterable[NotifyUpdated],
            conditions: Iterable[Callable[[], bool]],
            handlers: Iterable[Callable],
            all_conditions_to_be_true: bool = True,
            max_activation_count: int | None = None):

        self.observables: List[NotifyUpdated] = list(observables)
        self.conditions: List[Callable[[], bool]] = list(conditions)
        self.handlers: List[Callable] = list(handlers)
        self.all_conditions_to_be_true = all_conditions_to_be_true
        self.is_active: bool = True
        self.max_activation_count: int | None = max_activation_count
        self.done_activations: int = 0

        for observable in self.observables:
            observable.attach_on_update(self.observables_handler)

    def add_observable(self, observable: NotifyUpdated):
        """
        Appends an ``NotifyUpdated`` instance as a trigger to start
        conditions checking
        """

        self.observables.append(observable)
        observable.attach_on_update(self.observables_handler)

    def remove_observable(self, observable: NotifyUpdated):
        """
        Removes the ``NotifyUpdated`` instance from list of
        check triggers
        """

        self.observables.remove(observable)
        observable.detach_on_update(self.observables_handler)

    def observables_handler(self, placeholder: Any = 0):
        """
        Service method is subscribed to all using ``NotifyUpdated``  updates

        Checks ``is_active`` state and activation count limits, before
        handlers invokation
        """

        if not self.is_active:
            return

        if (self.max_activation_count is not None) and self.done_activations >= self.max_activation_count:
            return

        if self.all_conditions_to_be_true:
            if all(condition() for condition in self.conditions):
                self.done_activations += 1
                self.execute_all_handlers()

        elif any(condition() for condition in self.conditions):
            self.done_activations += 1
            self.execute_all_handlers()

    def execute_all_handlers(self):
        """
        A manual way to invoke all handlers without
        checking ``is_active`` and activation limits
        """

        for handler in self.handlers:
            handler()

    def __call__(self) -> Any:
        """
        Allows to invoke the condition is just a function
        is usable if target function is decorated by
        ``@invoke_when``

        :return: handler's value if count of handlers == 1,
        else returns a list of all handlers' values
        """

        if len(self.handlers) == 1:
            return self.handlers[0]()

        result: List[Any] = []
        for handler in self.handlers:
            result.append(handler())

        return result
