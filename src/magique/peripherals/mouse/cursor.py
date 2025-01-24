from mouse import get_position

from ....magique.declarative import NotifyUpdated


class MagiqueCursor(NotifyUpdated):
    def __init__(self):
        super().__init__()
        x, y = get_position()

        # that fields are updated automatically by general mouse hook
        self.x: int = x
        self.y: int = y
        self.monitor_id: int = 1     # Numeration is based on your PC display setup
                                     # and numbers given by your OS
                                     # Default display number in windows, linux and macOS =


