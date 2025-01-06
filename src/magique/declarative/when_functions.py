from typing import Iterable, Callable
from .when_condition import WhenCondition
from .observable import Observable


def when(observables: Observable | Iterable[Observable],
         conditions: Callable[[], bool] | Iterable[Callable[[], bool]],
         target_function: Callable | Iterable[Callable]) -> WhenCondition:

    if isinstance(observables, Observable):
        observables = [observables]

    if isinstance(conditions, Callable):
        conditions = [conditions]

    elif isinstance(target_function, Callable):
        target_function = [target_function]

    return WhenCondition(observables, conditions, target_function)
