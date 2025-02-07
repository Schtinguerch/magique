import time
from ...declarative import NotifyUpdated, notify_property_updated


class MagiqueWheel(NotifyUpdated):
    def __init__(self):
        super().__init__()
        self._delta: float = 0
        self.last_wheel_timestamp: float = 0.0

    @property
    def delta(self) -> float: return self._delta

    @delta.setter
    @notify_property_updated(lambda self: self._delta)
    def delta(self, new_delta: float): self._delta = new_delta
