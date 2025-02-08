from mouse import get_position, move

from ...declarative import NotifyUpdated, notify_property_updated


class MagiqueCursor(NotifyUpdated):
    def __init__(self):
        super().__init__()
        x, y = get_position()

        # used by hook to prevent looping
        self._move_cursor_on_property_set: bool = True

        # that fields are updated automatically by general mouse hook
        self._x: int = x
        self._y: int = y
        self._monitor_id: int = 1     # Numeration is based on your PC display setup
                                      # and numbers given by your OS
                                      # Default display number in windows, linux and macOS =

    @property
    def x(self) -> int: return self._x

    @x.setter
    @notify_property_updated(lambda self: self._x)
    def x(self, new_x: int):
        if self._move_cursor_on_property_set: move(new_x, self.y)
        self._x = new_x

    @property
    def y(self) -> int: return self._y

    @y.setter
    @notify_property_updated(lambda self: self._y)
    def y(self, new_y: int):
        if self._move_cursor_on_property_set: move(self.x, new_y)
        self._y = new_y

    @property
    def monitor_id(self) -> int: return self._monitor_id

    @monitor_id.setter
    @notify_property_updated(lambda self: self._monitor_id)
    def monitor_id(self, new_monitor_id: int): self._monitor_id = new_monitor_id
