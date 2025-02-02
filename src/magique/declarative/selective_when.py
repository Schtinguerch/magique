from typing import List, Callable, Any, Iterable, Dict
from .notify_updated import NotifyUpdated


class SelectiveWhenCondition:
    """
    The class responsible for catching ``NotifyUpdated`` events
    to start specified condition checking

    The selection is based on checking of value which function is returned.
    If function returns ``True``, its according handler function is invoking

    If conditions satisfied, specified functions are invoked
        1. ``observables`` - the collection of ``NotifyUpdated`` which updates are triggers to start conditions checking
        2. ``condition_handler_dict`` - the dictionary where key is condition ``func() -> bool``, value is handler
        3. ``all_conditions_to_be_true`` True - need all conditions return True, False - at least one returns True
        4. ``invoke_on_first_true_only`` - invokes only one function where condition returned True (first occur)
        5. ``max_activation_count`` - max count of ``handlers`` invokation if conditions are satisfied
    """

    def __init__(
            self,
            observables: Iterable[NotifyUpdated],
            condition_handler_dict: Dict[Callable[[], bool], Callable[[], Any]],
            invoke_on_first_true_only: bool = True,
            max_activation_count: int | None = None):

        self.observables: List[NotifyUpdated] = list(observables)
        self.condition_handler_dict = condition_handler_dict
        self.invoke_on_first_true_only = invoke_on_first_true_only
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

        at_least_one_condition_satisfied: bool = False
        for condition in self.condition_handler_dict:
            if not condition():
                continue

            self.condition_handler_dict[condition]()
            at_least_one_condition_satisfied = True

            if self.invoke_on_first_true_only:
                self.done_activations += 1
                break
        else:
            if at_least_one_condition_satisfied:
                self.done_activations += 1


def selective_when(
        observables: NotifyUpdated | Iterable[NotifyUpdated],
        conditions: Dict[Callable[[], bool], Callable[[], Any]],
        invoke_on_first_true_only: bool = True,
        max_activations: int | None = None) -> SelectiveWhenCondition:
    """
    Generates new instance of ``SelectiveWhenCondition``
    catching ``NotifyUpdated`` events to start specified condition checking

    The selection is based on checking of value which function is returned.
    If function returns ``True``, its according handler function is invoking

    If conditions satisfied, specified functions are invoked
        1. ``observables`` - the collection of ``NotifyUpdated`` which updates are triggers to start conditions check
        2. ``condition_handler_dict`` - the dictionary where key is condition ``func() -> bool``, value is handler
        3. ``all_conditions_to_be_true`` True - need all conditions return True, False - at least one returns True
        4. ``invoke_on_first_true_only`` - invokes only one function where condition returned True (first occur)
        5. ``max_activation_count`` - max count of ``handlers`` invokation if conditions are satisfied
    """

    if isinstance(observables, NotifyUpdated):
        observables = [observables]

    return SelectiveWhenCondition(observables, conditions, invoke_on_first_true_only, max_activations)
