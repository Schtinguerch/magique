from mouse import wheel
from ...declarative import NotifyUpdated, notify_property_updated


class MagiqueWheel(NotifyUpdated):
    def __init__(self):
        super().__init__()
        self._wheel_on_property_set: bool = True
        self._delta: float = 0
        self.last_wheel_timestamp: float = 0.0

    @property
    def delta(self) -> float: return self._delta

    @delta.setter
    @notify_property_updated(lambda self: self._delta)
    def delta(self, new_delta: float):
        if self._wheel_on_property_set: wheel(new_delta)
        self._delta = new_delta
