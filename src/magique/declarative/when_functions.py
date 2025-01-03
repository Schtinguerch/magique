from typing import List, Callable
from multipledispatch import dispatch
from .when_condition import WhenCondition
from .observable import Observable


@dispatch(Observable, Callable[[], bool], Callable)
def when(observable: Observable, condition: Callable[[], bool], target_function: Callable) -> WhenCondition:
    return WhenCondition([observable], [condition], [target_function])


@dispatch(List[Observable], Callable[[], bool], Callable)
def when(observables: List[Observable], condition: Callable[[], bool], target_function: Callable) -> WhenCondition:
    return WhenCondition(observables, [condition], [target_function])


@dispatch(List[Observable], List[Callable[[], bool]], List[Callable])
def when(
        observables: List[Observable],
        conditions: List[Callable[[], bool]],
        target_functions: List[Callable]) -> WhenCondition:
    return WhenCondition(observables, conditions, target_functions)
