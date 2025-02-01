from typing import Literal, Dict, Self, List, Tuple
from ...declarative import NotifyUpdated
import mouse


ButtonType = Literal["left", "right", "middle", "wheel"]


class MagiqueMouseButton(NotifyUpdated):
    def __init__(self, button_name: ButtonType):
        super().__init__()
        self.button = button_name

    def is_pressed(self):
        return mouse.is_pressed(self.button)

    def is_released(self):
        return not mouse.is_pressed(self.button)


class AnyMouseButton(MagiqueMouseButton):
    def __init__(self):
        super().__init__("left")
        self.pressed: bool = False

    def is_pressed(self) -> bool:
        return self.pressed

    def is_released(self) -> bool:
        return not self.pressed


class OneOfMouseButtons(MagiqueMouseButton):
    redirect_dict: Dict[MagiqueMouseButton, List[Self]] = {}

    # noinspection PyTypeChecker
    def __init__(self, *buttons: MagiqueMouseButton):
        super().__init__("")
        self.buttons: Tuple[MagiqueMouseButton] = buttons

        for button in self.buttons:
            if button in self.redirect_dict:
                self.redirect_dict[button].append(self)
            else:
                self.redirect_dict[button] = [self]

    def is_pressed(self) -> bool:
        return any(map(lambda k: k.is_pressed(), self.buttons))

    def is_released(self) -> bool:
        return all(map(lambda k: k.is_released(), self.buttons))
