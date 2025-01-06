from typing import List, Callable, Any, Iterable
from .observable import Observable


class WhenCondition:
    def __init__(
            self,
            observables: Iterable[Observable],
            conditions: Iterable[Callable[[], bool]],
            handlers: Iterable[Callable],
            all_conditions_to_be_true: bool = True):

        self.observables: List[Observable] = list(observables)
        self.conditions: List[Callable[[], bool]] = list(conditions)
        self.handlers: List[Callable] = list(handlers)
        self.all_conditions_to_be_true = all_conditions_to_be_true
        self.is_active: bool = True

        for observable in self.observables:
            observable.attach_on_update(self.observables_handler)

    def add_observable(self, observable: Observable):
        self.observables.append(observable)
        observable.attach_on_update(self.observables_handler)

    def remove_observable(self, observable: Observable):
        self.observables.remove(observable)
        observable.detach_on_update(self.observables_handler)

    def observables_handler(self, placeholder: Any = 0):
        if not self.is_active:
            return

        if self.all_conditions_to_be_true:
            if all(condition() for condition in self.conditions):
                self.execute_all_handlers()

        elif any(condition() for condition in self.conditions):
            self.execute_all_handlers()

    def execute_all_handlers(self):
        for handler in self.handlers:
            handler()
