from typing import Literal
import mouse


ButtonType = Literal["left", "right", "middle", "wheel"]


class MagiqueMouseButton:
    def __init__(self, button_name: ButtonType):
        self.button = button_name

    def is_pressed(self):
        return mouse.is_pressed(self.button)

    def is_released(self):
        return not mouse.is_pressed(self.button)
