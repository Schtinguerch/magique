from abc import ABC, abstractmethod
from ..declarative import Observable


class Animation(ABC):
    def __init__(
            self,
            target: Observable,
            auto_revert: bool = False,
            repeat_count: int | None = 1):

        self.target: Observable = target
        self.auto_revert: bool = auto_revert
        self.repeat_count: int | None = repeat_count
        self.is_active: bool = False
        self.stop_signal: bool = False

    @abstractmethod
    def start(self, stop_running_animation: bool = False): pass

    def pause(self): self.is_active = False

    def resume(self): self.is_active = True

    @abstractmethod
    def reset(self): pass

    @abstractmethod
    def skip(self): pass

    @abstractmethod
    def wait_until_done(self): pass
