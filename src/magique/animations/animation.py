from typing import Any
from threading import Thread, Lock

from abc import ABC, abstractmethod
from ..declarative import Observable


class Animation(ABC):
    lock = Lock()

    def __init__(
            self,
            target: Observable,
            from_value: Any = None,
            to_value: Any = None,
            auto_revert: bool = False,
            repeat_count: int | None = 1):

        self.animation_thread: Thread = self._new_animation_thread()

        self.from_value: Any = from_value or target.value
        self.to_value: Any = to_value or target.value

        self.target: Observable = target
        self.auto_revert: bool = auto_revert
        self.repeat_count: int | None = repeat_count
        self.is_active: bool = False
        self.stop_signal: bool = False

    @abstractmethod
    def _animation_loop(self, is_backward: bool = False): pass

    def start(self, stop_running_animation: bool = False):
        """
        Enables the animation thread. If animation thread is enabled,
        it can stop it and start new animation thread

        :param stop_running_animation: If `True` the running thread will be stopped,
        else the running thread stays running, new animation not starting
        """

        self.lock.acquire()
        if self.is_active:
            if not stop_running_animation:
                if self.animation_thread.is_alive():
                    self.lock.release()
                    return

            self.reset()

        try:
            self.is_active = True
            self.animation_thread.start()

        finally:
            self.lock.release()

    def pause(self):
        """
        Pauses the animation, with ability to resume when it's needed
        """

        self.is_active = False

    def resume(self):
        """
        Resumes the paused animation
        """

        self.is_active = True

    def reset(self):
        """
        Stops the animation thread and sets target value = start animation value (``from_value``)
        """

        self._stop_animation_thread()
        self.target.value = self.from_value

    def skip(self):
        """
        Stops the animation thread and sets target value = end animation value (``to_value``)
        """

        self._stop_animation_thread()
        self.target.value = self.to_value

    def wait_until_done(self):
        """
        Joins the animation thread (make you to wait until the animation done)
        """

        self.animation_thread.join()

    def _stop_animation_thread(self):
        self.is_active = False
        self.stop_signal = True
        self.animation_thread.join()
        self.animation_thread = self._new_animation_thread()
        self.stop_signal = False

    def _new_animation_thread(self) -> Thread:
        animation_thread = Thread(target=self._animate)
        animation_thread.daemon = True
        return animation_thread

    def _animate(self):
        if self.repeat_count is None:
            while not self.stop_signal:
                self._animation_iteration()

        repeat_iterations: int = 0
        while not self.stop_signal and repeat_iterations < self.repeat_count:
            self._animation_iteration()
            repeat_iterations += 1

    def _animation_iteration(self):
        self._animation_loop()
        if self.auto_revert:
            self._animation_loop(is_backward=True)
