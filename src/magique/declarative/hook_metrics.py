from .notify_updated import NotifyUpdated
from .observable import Observable
from typing import Callable, TypeVar, List, Any
from queue import Queue


T = TypeVar('T')
_sentinel: Any = object()


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
            metrics_iteration_function: Callable[[], T] = _sentinel,
            initial_value: T | None = None,
            start_immediately: bool = False,
            *triggers: NotifyUpdated):

        super().__init__(initial_value)
        self.updates_queue: Queue[T] = Queue()
        self.listening: bool = False
        self.triggers: List[NotifyUpdated] = list(triggers)

        if metrics_iteration_function is not _sentinel:
            self.metrics_iteration: Callable[[], T] = metrics_iteration_function

        if start_immediately:
            self.start_metrics_hooks()

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

    def __call__(self) -> T:
        return self.metrics_iteration()


def hook_obs(
        *triggers: NotifyUpdated,
        metrics_function: Callable[[], T] | None = None,
        initial_value: T | None = None,
        start_immediately: bool = False) -> HookMetrics:
    """
    Creates an instance of HookMetrics class
    :param metrics_function: calculator of new metrics value
    :param initial_value: start value to be initialized
    :param triggers: NotifyUpdated instances, invokation of its ``raise_update_event()``
    is a trigger to invoke ``metrics_iteration_function()``
    :param start_immediately: if equals ``True`` the ``start_hook_metrics()``
    invokes immediately
    """

    return HookMetrics(metrics_function, initial_value, start_immediately, *triggers)


def hook_metrics(
        *triggers: NotifyUpdated,
        initial_value: T | None = None,
        start_immediately: bool = False):
    """
    A decorator creating an instance of HookMetrics class
    :param initial_value: start value to be initialized
    :param triggers: NotifyUpdated instances, invokation of its ``raise_update_event()``
    is trigger to invoke ``metrics_iteration_function()``
    :param start_immediately: if equals ``True`` the ``start_hook_metrics()``
    invokes immediately

    The returned ``HookMetrics`` allows direct call () via ``__call__()`` the
    magic method
    """

    def decorator(metrics_iteration_function: Callable[[], T]) -> HookMetrics:
        return HookMetrics(metrics_iteration_function, initial_value, start_immediately, *triggers)

    return decorator
