from typing import List, Callable
from .when_condition import WhenCondition
from .observable import Observable


def when(observables: Observable | List[Observable],
         conditions: Callable[[], bool] | List[Callable[[], bool]],
         target_function: Callable | List[Callable]) -> WhenCondition:

    if isinstance(observables, Observable):
        observables = [observables]

    if isinstance(conditions, Callable):
        conditions = [conditions]

    elif isinstance(target_function, Callable):
        target_function = [target_function]

    return WhenCondition(observables, conditions, target_function)
