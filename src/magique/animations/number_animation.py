from typing import Callable, Any
from threading import Thread, Lock
from time import time, sleep

from ..declarative import Observable
from .animation import Animation
from .easing_functions import linear


Number = int | float


class NumberAnimation(Animation):
    """
    Allows animate ``Observable`` variables between two values with
    wide configuration options

     - ``from_value`` and ``to_value`` - it's the animated range for target object
     - ``easing_function`` - by default is linear, allows special smoothing, function accepts and returns value in [0;1]
     - ``duration_sec`` - animation duration in seconds
     - ``fps`` - frames (iterations) per second, by default = 30
     - ``converter`` - function to convert the numeric value to the required value, your object supports
     - ``auto_revert`` - if ``True`` after direct animation, starts reversed animation
     - ``repeat_count`` - set up for repeat policy. In default = 1, if `None` the animation loop is endless
    """

    lock = Lock()

    def __init__(
            self,
            target: Observable,
            from_value: Number | None = None,
            to_value: Number | None = None,
            easing_function: Callable[[float], float] = linear,
            duration_sec: float = 1.0,
            fps: float = 30.0,
            converter: Callable[[Any], Any] = lambda x: x,
            auto_revert: bool = False,
            repeat_count: int | None = 1):

        super().__init__(target, auto_revert, repeat_count)
        self.animation_thread: Thread = self._new_animation_thread()

        self.from_value: Number = from_value or target.value
        self.to_value: Number = to_value or target.value
        self.easing_function: Callable[[float], float] = easing_function
        self.duration_sec: float = duration_sec
        self.fps: float = fps
        self.converter: Callable[[Any], Any] = converter
        self.current_value: Number = self.from_value

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
        animation_thread = Thread(target=self._animate_number)
        animation_thread.daemon = True
        return animation_thread

    def _animate_number(self):
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

    def _animation_loop(self, is_backward: bool = False):
        frame_time_seconds: float = 1 / self.fps
        total_frames: int = int(self.duration_sec * self.fps)
        delta: float = self.to_value - self.from_value

        if total_frames == 0:
            total_frames = 1

        start_time = time()
        reached_frames: int = 0
        while not self.stop_signal and reached_frames < total_frames:
            if not self.is_active:
                sleep(frame_time_seconds)
                continue

            elapsed_time: float = time() - start_time

            if is_backward:
                progress: float = 1 - (elapsed_time / self.duration_sec)
                if progress < 0: progress = 0
            else:
                progress: float = elapsed_time / self.duration_sec
                if progress > 1.0: progress = 1.0

            eased_value: float = self.easing_function(progress)
            self.current_value = self.from_value + self.converter(delta * eased_value)
            self.target.value = self.current_value

            sleep(frame_time_seconds)
            reached_frames += 1
