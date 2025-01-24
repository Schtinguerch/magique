from screeninfo import Monitor
from typing import List, Final

from ....magique.declarative import NotifyUpdated, ObservableList


class MonitorInfo(NotifyUpdated):
    def __init__(self, info: Monitor):
        super().__init__()
        self._x: int = info.x
        self._y: int = info.y
        self._width: int = info.width
        self._height: int = info.height

    @property
    def x(self) -> int: return self._x

    @x.setter
    def x(self, new_x: int):
        old_x: int = self._x
        self._x = new_x
        self.raise_update_if_values_diff(old_x, new_x)

    @property
    def y(self) -> int: return self._y

    @y.setter
    def y(self, new_y: int):
        old_y: int = self._y
        self._y = new_y
        self.raise_update_if_values_diff(old_y, new_y)

    @property
    def width(self) -> int: return self._width

    @width.setter
    def width(self, new_width: int):
        old_width: int = self._width
        self._width = new_width
        self.raise_update_if_values_diff(old_width, new_width)

    @property
    def height(self) -> int: return self._height

    @height.setter
    def height(self, new_height: int):
        old_height: int = self._height
        self._height = new_height
        self.raise_update_if_values_diff(old_height, new_height)


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

    def detach_all_handlers(self) -> None:
        super().detach_all_handlers()
        self.monitors.detach_on_update(self._handler)
