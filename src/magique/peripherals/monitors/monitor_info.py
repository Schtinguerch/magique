from screeninfo import Monitor
from typing import List, Final, Any

from ....magique.declarative import NotifyUpdated, ObservableList, notify_property_updated


class MonitorInfo(NotifyUpdated):
    def __init__(self, info: Monitor):
        super().__init__()
        self._x: int = info.x
        self._y: int = info.y
        self._width: int = info.width
        self._height: int = info.height
        self._name: str = info.name
        self._is_primary: bool = info.is_primary

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

    @property
    def name(self) -> str: return self._name

    @name.setter
    @notify_property_updated(lambda self: self._name)
    def name(self, new_name: str): self._name = new_name

    @property
    def is_primary(self) -> bool: return self._is_primary

    @is_primary.setter
    @notify_property_updated(lambda self: self._is_primary)
    def is_primary(self, new_is_primary: bool): self._is_primary = new_is_primary

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MonitorInfo):
            return False

        return (
            self.x == other.x
            and self.y == other.y
            and self.width == other.width
            and self.height == other.height
            and self.name == other.name
            and self.is_primary == other.is_primary
        )

    def __repr__(self) -> str:
        class_name: str = self.__class__.__name__
        return (
            f"<{class_name}: '{self.name}', primary={self.is_primary}, "
            f"xy={self.x};{self.y}, resolution={self.width}x{self.height} >"
        )

    def __str__(self) -> str:
        return self.__repr__()


class MonitorSetup(NotifyUpdated):
    def __init__(self, monitors: List[Monitor] | None = None):
        super().__init__()
        self._handler = lambda _: self.raise_update_event()
        self._connected_monitors: List[MonitorInfo] = []
        self._disconnected_monitors: List[MonitorInfo] = []

        monitors_info = None
        if monitors is not None:
            monitors_info = [MonitorInfo(m) for m in monitors]

        self.monitors: Final[ObservableList[MonitorInfo]] = ObservableList(monitors_info)
        self.monitors.attach_on_update(self._handler)

    @property
    def connected_monitors(self) -> List[MonitorInfo]:
        return self._connected_monitors

    @connected_monitors.setter
    @notify_property_updated(lambda self: self._connected_monitors)
    def connected_monitors(self, new_connected_monitors: List[MonitorInfo]):
        self._connected_monitors = new_connected_monitors

    @property
    def disconnected_monitors(self) -> List[MonitorInfo]:
        return self._disconnected_monitors

    @disconnected_monitors.setter
    @notify_property_updated(lambda self: self._disconnected_monitors)
    def disconnected_monitors(self, new_disconnected_monitors: List[MonitorInfo]):
        self._disconnected_monitors = new_disconnected_monitors

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

    def update(self, monitors: List[Monitor]):
        monitors_info = [MonitorInfo(m) for m in monitors]
        if self.monitors.value == monitors_info:
            return

        monitor_names_before = [mi.name for mi in monitors_info]
        monitor_names_after = [mi.name for mi in self.monitors]

        added_monitor_names = [name for name in monitor_names_after if name not in monitor_names_before]
        removed_monitor_names = [name for name in monitor_names_before if name not in monitor_names_after]
        stayed_monitor_names = [name for name in monitor_names_before if name in monitor_names_after]

        self.connected_monitors = [mi for mi in monitors_info if mi.name in added_monitor_names]
        self.disconnected_monitors = [mi for mi in self.monitors if mi.name in removed_monitor_names]

        before_update_monitors = [mi for mi in self.monitors if mi.name in stayed_monitor_names]
        after_update_monitors = [mi for mi in monitors_info if mi.name in stayed_monitor_names]

        assert len(before_update_monitors) == len(after_update_monitors)
        for i in range(0, len(before_update_monitors)):
            before: MonitorInfo = before_update_monitors[i]
            after: MonitorInfo = after_update_monitors[i]

            before.x = after.x
            before.y = after.y
            before.height = after.height
            before.width = after.width
            before.is_primary = after.is_primary

        if len(self.connected_monitors) > 0:
            self.monitors.extend(self.connected_monitors)

        if len(self.disconnected_monitors) > 0:
            self.monitors.remove_many(self.disconnected_monitors)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MonitorSetup):
            return False

        return self.monitors == other.monitors
