from typing import Final, List, Dict
from .button import MagiqueMouseButton, OneOfMouseButtons, AnyMouseButton


Left: Final[MagiqueMouseButton] = MagiqueMouseButton("left")
Right: Final[MagiqueMouseButton] = MagiqueMouseButton("right")
Middle: Final[MagiqueMouseButton] = MagiqueMouseButton("middle")
Wheel: Final[MagiqueMouseButton] = MagiqueMouseButton("wheel")

LeftOrRight: Final[OneOfMouseButtons] = OneOfMouseButtons(Left, Right)
MiddleOrWheel: Final[OneOfMouseButtons] = OneOfMouseButtons(Middle, Wheel)

Any: Final[AnyMouseButton] = AnyMouseButton()
all_buttons: Final[List[MagiqueMouseButton]] = [Left, Right, Middle, Wheel]

str_button_dict: Dict[str, MagiqueMouseButton] = {}
for button in all_buttons:
    if button.button in str_button_dict: continue
    str_button_dict[button.button] = button
