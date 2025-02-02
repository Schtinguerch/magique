from typing import Iterable, Callable, Any, Tuple
from .when_condition import WhenCondition
from .notify_updated import NotifyUpdated
from .observable import Observable


def when(observables: NotifyUpdated | Iterable[NotifyUpdated],
         conditions: Callable[[], bool] | Iterable[Callable[[], bool]],
         target_functions: Callable | Iterable[Callable],
         all_conditions_to_be_true: bool = True,
         max_activation_count: int | None = None) -> WhenCondition:
    """
    Creates a new instance of ``WhenCondition``, starts a hook for
    passed ``NotifyUpdated`` updates starting passed conditions checking

    If conditions are satisfied, the target functions are invoked

    :param observables: the collection of ``NotifyUpdated`` which updates are triggers to start conditions checking
    :param conditions: the collection of ``func() -> bool`` with some checks, True = condition is satisfied
    :param target_functions: the collection of ``func()`` with some behavior if conditions are satisfied
    :param all_conditions_to_be_true: True - need all conditions return True, False - at least one returns True
    :param max_activation_count: max count of ``handlers`` invokation if conditions are satisfied
    :return: new ``WhenCondition`` instance
    """

    if isinstance(observables, NotifyUpdated):
        observables = [observables]

    if isinstance(conditions, Callable):
        conditions = [conditions]

    if isinstance(target_functions, Callable):
        target_functions = [target_functions]

    return WhenCondition(observables, conditions, target_functions, all_conditions_to_be_true, max_activation_count)


def invoke_when(observables: NotifyUpdated | Iterable[NotifyUpdated] = tuple(),
                conditions: Callable[[], bool] | Iterable[Callable[[], bool]] = tuple(),
                all_conditions_to_be_true: bool = True,
                max_activation_count: int | None = None):
    """
    A decorator which subscribes your function to a hook for
    passed ``NotifyUpdated`` updates starting passed conditions checking

    If conditions are satisfied, the decorated function is invoked

    :param observables: the collection of ``NotifyUpdated`` which updates are triggers to start conditions checking
    :param conditions: the collection of ``func() -> bool`` with some checks, True = condition is satisfied
    :param all_conditions_to_be_true: True - need all conditions return True, False - at least one returns True
    :param max_activation_count: max count of ``handlers`` invokation if conditions are satisfied
    :return: new ``WhenCondition`` instance. It supports direct calls via magic method ``__call__()``
    """

    if (isinstance(observables, Observable)
            and isinstance(conditions, Tuple)
            and len(conditions) == 0):

        obs: Observable = observables
        conditions = (lambda: obs.value,)

    def decorator(target_handler: Callable[[], Any]) -> WhenCondition:
        return when(
            observables,
            conditions,
            target_handler,
            all_conditions_to_be_true,
            max_activation_count
        )

    return decorator


def with_observables(*observables: NotifyUpdated):
    def decorator(when_condition: WhenCondition) -> WhenCondition:
        for observable in observables:
            when_condition.add_observable(observable)
        return when_condition

    return decorator
