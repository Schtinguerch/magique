from .notify_updated import NotifyUpdated
from .observable import Observable
from typing import Callable, TypeVar, List, Any
from queue import Queue


T = TypeVar('T')


class HookMetrics(Observable[T]):
    def __init__(
            self,
            metrics_iteration_function: Callable[[], T] | None = None,
            initial_value: T | None = None,
            *triggers: NotifyUpdated):

        super().__init__(initial_value)
        self.updates_queue: Queue[T] = Queue()
        self.listening: bool = False
        self.triggers: List[NotifyUpdated] = list(triggers)

        if metrics_iteration_function is not None:
            self.metrics_iteration: Callable[[], T] = metrics_iteration_function

    def start_metrics_hooks(self) -> None:
        if self.listening:
            return

        self.listening = True
        for trigger in self.triggers:
            trigger += self.notify_updated_handler

    def stop_metrics_hooks(self) -> None:
        if not self.listening:
            return

        self.listening = False
        for trigger in self.triggers:
            trigger -= self.notify_updated_handler

    def notify_updated_handler(self, placeholder: Any) -> None:
        self.value = self.metrics_iteration()

    def metrics_iteration(self) -> T:
        pass


def hook_obs(
        metrics_iteration_function: Callable[[], T] | None = None,
        initial_value: T | None = None,
        *triggers: NotifyUpdated) -> HookMetrics:

    return HookMetrics(metrics_iteration_function, initial_value, *triggers)
