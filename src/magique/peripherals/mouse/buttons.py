from typing import Final, List, Dict
from .button import MagiqueMouseButton, OneOfMouseButtons, AnyMouseButton
from .cursor import MagiqueCursor


Cursor: Final[MagiqueCursor] = MagiqueCursor()

Left: Final[MagiqueMouseButton] = MagiqueMouseButton("left")
Right: Final[MagiqueMouseButton] = MagiqueMouseButton("right")
Middle: Final[MagiqueMouseButton] = MagiqueMouseButton("middle")
WheelButton: Final[MagiqueMouseButton] = MagiqueMouseButton("wheel")

LeftOrRight: Final[OneOfMouseButtons] = OneOfMouseButtons(Left, Right)
MiddleOrWheel: Final[OneOfMouseButtons] = OneOfMouseButtons(Middle, WheelButton)

Any: Final[AnyMouseButton] = AnyMouseButton()
all_buttons: Final[List[MagiqueMouseButton]] = [Left, Right, Middle, WheelButton]

str_button_dict: Dict[str, MagiqueMouseButton] = {}
for button in all_buttons:
    if button.button in str_button_dict: continue
    str_button_dict[button.button] = button
