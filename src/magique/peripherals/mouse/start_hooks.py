from time import time
from typing import List, Literal

from . import MagiqueMouseButton, OneOfMouseButtons, str_button_dict, Any, Cursor, Wheel
from ..monitors import monitor_setup, auto_init_monitor_setup, MonitorInfo, MonitorSetup

from mouse import hook, ButtonEvent, MoveEvent, WheelEvent


now_pressed_buttons: List[MagiqueMouseButton] = []
auto_init_monitor_setup()


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
    Cursor._move_cursor_on_property_set = False
    Cursor.x = event.x
    Cursor.y = event.y
    Cursor._move_cursor_on_property_set = True

    monitor_screen_is_on: MonitorInfo = monitor_setup.get_monitor_cursor_is_on(Cursor.x, Cursor.y)
    Cursor.monitor_id = monitor_setup.monitors.value.index(monitor_screen_is_on) + 1


def on_wheel_event(event: WheelEvent):
    timestamp: float = float(time())
    Wheel._wheel_on_property_set = False
    if timestamp - Wheel.last_wheel_timestamp < 0.5:
        Wheel.delta += event.delta
    else:
        Wheel.delta = event.delta

    Wheel.last_wheel_timestamp = timestamp
    Wheel._wheel_on_property_set = True


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
