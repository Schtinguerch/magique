from screeninfo import Monitor
from typing import List, Final

from ....magique.declarative import NotifyUpdated, ObservableList, notify_property_updated


class MonitorInfo(NotifyUpdated):
    def __init__(self, info: Monitor):
        super().__init__()
        self._x: int = info.x
        self._y: int = info.y
        self._width: int = info.width
        self._height: int = info.height

    def is_cursor_inside(self, position_x: int, position_y: int) -> bool:
        inside_x: bool = self.x <= position_x < self.x + self.width
        inside_y: bool = self.y <= position_y < self.y + self.height
        return inside_x and inside_y

    @property
    def x(self) -> int: return self._x

    @x.setter
    @notify_property_updated(lambda self: self._x)
    def x(self, new_x: int): self._x = new_x

    @property
    def y(self) -> int: return self._y

    @y.setter
    @notify_property_updated(lambda self: self._y)
    def y(self, new_y: int): self._y = new_y

    @property
    def width(self) -> int: return self._width

    @width.setter
    @notify_property_updated(lambda self: self._width)
    def width(self, new_width: int): self._width = new_width

    @property
    def height(self) -> int: return self._height

    @height.setter
    @notify_property_updated(lambda self: self._height)
    def height(self, new_height: int): self._height = new_height


class MonitorSetup(NotifyUpdated):
    def __init__(self, monitors: List[Monitor] | None = None):
        super().__init__()
        self._handler = lambda _: self.raise_update_event()

        monitors_info = None
        if monitors is not None:
            monitors_info = [MonitorInfo(m) for m in monitors]

        self.monitors: Final[ObservableList] = ObservableList(monitors_info)
        self.monitors.attach_on_update(self._handler)

    def reinit(self, monitors: List[Monitor] | None = None):
        if monitors is None:
            return

        monitors_info = [MonitorInfo(m) for m in monitors]
        self.monitors.no_event_set_value(monitors_info)

    def get_monitor_cursor_is_on(self, x: int, y: int) -> MonitorInfo:
        for monitor in self.monitors.value:
            if monitor.is_cursor_inside(x, y):
                return monitor

        return self.monitors[0]

    def detach_all_handlers(self) -> None:
        super().detach_all_handlers()
        self.monitors.detach_on_update(self._handler)
