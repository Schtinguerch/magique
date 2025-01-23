import time

from .observable import Observable
from typing import Callable, TypeVar, Tuple
from threading import Thread, Lock
from queue import Queue


T = TypeVar('T')


class LoopMetrics(Observable[T]):
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

        if metrics_iteration_function is not None:
            self.metrics_iteration: Callable[[], T] = metrics_iteration_function

    def reinitialize_threads(self) -> Tuple[Thread, Thread]:
        listening_thread = Thread(target=self.listen_updates)
        listening_thread.daemon = True

        handling_thread = Thread(target=self.handle_updates)
        handling_thread.daemon = True

        return listening_thread, handling_thread

    def start_metrics_loop(self) -> None:
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
        self.lock.acquire()

        if not self.listening:
            self.lock.release()
            return

        self.listening = False
        self.listening_thread.join()
        self.handling_thread.join()

        self.listening_thread, self.handling_thread = self.reinitialize_threads()
        self.lock.release()

    def listen_updates(self) -> None:
        while True:
            if not self.listening: break
            time.sleep(self.loop_delay_seconds)

            new_value: T = self.metrics_iteration()
            self.updates_queue.put(new_value)

    def handle_updates(self) -> None:
        while True:
            if not self.listening: break
            if self.updates_queue.empty(): continue

            self.value = self.updates_queue.get_nowait()
            self.updates_queue.task_done()

    def metrics_iteration(self) -> T:
        pass


def loop_obs(
        metrics_iteration_function: Callable[[], T] | None = None,
        initial_value: T | None = None,
        loop_delay_seconds: float = 0.) -> LoopMetrics:

    return LoopMetrics(metrics_iteration_function, initial_value, loop_delay_seconds)
