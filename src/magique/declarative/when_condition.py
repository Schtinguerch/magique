from typing import List, Callable, Any, Iterable
from .notify_updated import NotifyUpdated


class WhenCondition:
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
        self.observables.append(observable)
        observable.attach_on_update(self.observables_handler)

    def remove_observable(self, observable: NotifyUpdated):
        self.observables.remove(observable)
        observable.detach_on_update(self.observables_handler)

    def observables_handler(self, placeholder: Any = 0):
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
        for handler in self.handlers:
            handler()
