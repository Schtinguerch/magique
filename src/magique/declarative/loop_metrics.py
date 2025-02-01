import time

from .observable import Observable
from typing import Callable, TypeVar, Tuple, Any
from threading import Thread, Lock
from queue import Queue


T = TypeVar('T')


class LoopMetrics(Observable[T]):
    """
    The class invoking specified function in loop
    by specified delay (default delay = 0.5s)

    When specified function calculated value different
    to previous calculated value, the ``raise_update_event()``
    is invoked from that class instance

    You can create your custom class inherited from LoopMetrics
    and override the method ``metrics_iteration()``.

    If you want save the in-coded function, in __init__,
    you can set ``metrics_iteration_function`` value = None, calling
    ``super().__init__(initial_value, initial_value=None, *triggers)``

    By default, if in value queue value = None is found, the handling
    thread stops its working. If you need to avoid metrics stopping
    when your ``metrics_iteration_function`` returns None, you
    need to set ``self.terminate_queue_value`` = your new value,
    which the metrics function will return never
    """

    lock = Lock()

    def __init__(
            self,
            metrics_iteration_function: Callable[[], T] | None = None,
            initial_value: T | None = None,
            loop_delay_seconds: float = 0.5):

        super().__init__(initial_value)
        self.updates_queue: Queue[T] = Queue()
        self.listening: bool = False
        self.loop_delay_seconds: float = loop_delay_seconds
        self.listening_thread, self.handling_thread = self.reinitialize_threads()
        self.terminate_queue_value: Any = None

        if metrics_iteration_function is not None:
            self.metrics_iteration: Callable[[], T] = metrics_iteration_function

    def reinitialize_threads(self) -> Tuple[Thread, Thread]:
        listening_thread = Thread(target=self.listen_updates)
        listening_thread.daemon = True

        handling_thread = Thread(target=self.handle_updates)
        handling_thread.daemon = True

        return listening_thread, handling_thread

    def start_metrics_loop(self) -> None:
        """
        Enables using metrics, starting two threads with loops
        if the method wasn't used before, listening is/was stopped

        The 1st loop is reading ``metrics_iteration_function`` value and passing to the queue

        The 2nd loop is reading the value queue and invoking ``raise_update_event`` if last
        calculated value is different to previous value
        """

        self.lock.acquire()
        if self.listening:
            self.lock.release()
            return

        try:
            self.listening = True
            self.listening_thread.start()
            self.handling_thread.start()

        finally:
            self.lock.release()

    def stop_metrics_loop(self) -> None:
        """
        Stops using metrics, stopping running loops if listening is enabled
        """

        self.lock.acquire()

        if not self.listening:
            self.lock.release()
            return

        self.listening = False
        self.updates_queue.put(self.terminate_queue_value)

        self.listening_thread.join()
        self.handling_thread.join()

        self.listening_thread, self.handling_thread = self.reinitialize_threads()
        self.lock.release()

    def listen_updates(self) -> None:
        """
        Loop No.1 - get values from ``metrics_iteration_function`` by delay
        and passing values to the queue
        """

        while True:
            if not self.listening: break
            time.sleep(self.loop_delay_seconds)

            new_value: T = self.metrics_iteration()
            self.updates_queue.put(new_value)

    def handle_updates(self) -> None:
        """
        Loop No.2 - get values queue, populated from Loop No.1
        and passing that into ``self.value`` property. The property
        invokes ``raise_update_event`` if new value is different to
        the previous value
        """

        while True:
            value = self.updates_queue.get()
            if value == self.terminate_queue_value:
                self.updates_queue.task_done()
                break

            self.value = value
            self.updates_queue.task_done()

    def metrics_iteration(self) -> T:
        """
        By default, it's empty function, but you can
        override it in your own child class
        :return: A value calculated by the function, update of that
        you want to catch and create according event
        """
        pass


def loop_obs(
        metrics_iteration_function: Callable[[], T] | None = None,
        initial_value: T | None = None,
        loop_delay_seconds: float = 0.5) -> LoopMetrics:
    """
    Creates an instance of LoopMetrics class
    :param metrics_iteration_function: calculator of new metrics value
    :param initial_value: start value to be initialized
    :param loop_delay_seconds: the time to wait in loop before invoke
    the ``metrics_iteration_function``. By default, equals 0.5s
    """

    return LoopMetrics(metrics_iteration_function, initial_value, loop_delay_seconds)
