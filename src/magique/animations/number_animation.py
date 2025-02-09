from typing import Callable, Any
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

        super().__init__(target, from_value, to_value, auto_revert, repeat_count)

        self.from_value: Number = from_value or target.value
        self.to_value: Number = to_value or target.value
        self.easing_function: Callable[[float], float] = easing_function
        self.duration_sec: float = duration_sec
        self.fps: float = fps
        self.converter: Callable[[Any], Any] = converter

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
            self.target.value = self.from_value + self.converter(delta * eased_value)

            sleep(frame_time_seconds)
            reached_frames += 1
