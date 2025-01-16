from typing import Iterable, Callable
from .when_condition import WhenCondition
from .notify_updated import NotifyUpdated


def when(observables: NotifyUpdated | Iterable[NotifyUpdated],
         conditions: Callable[[], bool] | Iterable[Callable[[], bool]],
         target_functions: Callable | Iterable[Callable],
         max_activation_count: int | None = None) -> WhenCondition:

    if isinstance(observables, NotifyUpdated):
        observables = [observables]

    if isinstance(conditions, Callable):
        conditions = [conditions]

    if isinstance(target_functions, Callable):
        target_functions = [target_functions]

    return WhenCondition(observables, conditions, target_functions, max_activation_count)
