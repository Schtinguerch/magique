from typing import List, Literal
from . import MagiqueMouseButton, OneOfMouseButtons, str_button_dict, Any

from mouse import hook, ButtonEvent, MoveEvent, WheelEvent


now_pressed_buttons: List[MagiqueMouseButton] = []


def on_button_event(event: ButtonEvent):
    key_action: Literal["down", "up"] | None = event.event_type

    if event.button in str_button_dict:
        button: MagiqueMouseButton = str_button_dict[event.button]
        button.raise_update_event()

        if button in OneOfMouseButtons.redirect_dict:
            for dir_button in OneOfMouseButtons.redirect_dict[button]:
                dir_button.raise_update_event()

    Any.pressed = key_action == "down"
    Any.raise_update_event()


def on_move_event(event: MoveEvent):
    #raise NotImplementedError()
    pass


def on_wheel_event(event: WheelEvent):
    #raise NotImplementedError()
    pass


def on_any_button(event: ButtonEvent | MoveEvent | WheelEvent) -> None:
    if isinstance(event, MoveEvent):
        on_move_event(event)
        return

    if isinstance(event, ButtonEvent):
        on_button_event(event)
        return

    if isinstance(event, WheelEvent):
        on_wheel_event(event)
        return

    raise ValueError("what is the fucking event is here ?")


hook(on_any_button)
