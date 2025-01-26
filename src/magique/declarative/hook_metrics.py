from .notify_updated import NotifyUpdated
from .observable import Observable
from typing import Callable, TypeVar, List, Any
from queue import Queue


T = TypeVar('T')


class HookMetrics(Observable[T]):
    """
    The class invoking specified function when one
    of using NotifyUpdated instances has an event
    (invoked ``raise_update_event()``)

    When specified function calculated value different
    to previous calculated value, the ``raise_update_event()``
    is invoked from that class instance

    You can create your custom class inherited from HookMetrics
    and override the method ``metrics_iteration()``.

    If you want save the in-coded function, in __init__,
    you can set ``metrics_iteration_function`` value = None, calling
    ``super().__init__(initial_value, initial_value=None, *triggers)``
    """

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
        """
        Enables using hooks, calling ``attach_on_update`` of using NotifyUpdated instances
        if the method wasn't used before, listening is/was stopped
        """

        if self.listening:
            return

        self.listening = True
        for trigger in self.triggers:
            trigger += self.notify_updated_handler

    def stop_metrics_hooks(self) -> None:
        """
        Stops using hook, calling ``detach_on_update`` of using NotifyUpdated instances
        if listening is enabled
        """

        if not self.listening:
            return

        self.listening = False
        for trigger in self.triggers:
            trigger -= self.notify_updated_handler

    def notify_updated_handler(self, placeholder: Any) -> None:
        self.value = self.metrics_iteration()

    def metrics_iteration(self) -> T:
        """
        By default, it's empty function, but you can
        override it in your own child class
        :return: A value calculated by the function, update of that
        you want to catch and create according event
        """
        pass


def hook_obs(
        metrics_iteration_function: Callable[[], T] | None = None,
        initial_value: T | None = None,
        *triggers: NotifyUpdated) -> HookMetrics:
    """
    Creates an instance of HookMetrics class
    :param metrics_iteration_function: calculator of new metrics value
    :param initial_value: start value to be initialized
    :param triggers: NotifyUpdated instances, invokation of its ``raise_update_event()``
    is trigger to invoke ``metrics_iteration_function()``
    """

    return HookMetrics(metrics_iteration_function, initial_value, *triggers)
