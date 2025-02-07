import mouse
import random
import time

from .button import MagiqueMouseButton, AnyMouseButton, OneOfMouseButtons
from .buttons import all_buttons


def _press_and_release(button_name: str, hold_seconds: float | None = None) -> None:
    mouse.press(button_name)
    if hold_seconds is not None: time.sleep(hold_seconds)
    mouse.release(button_name)


def press(*buttons: MagiqueMouseButton, hold_seconds: float | None = None) -> None:
    """
    Presses and releases specified buttons by order (not a button combo)
    :param hold_seconds: time to hold the button pressed, by default release is done immediately
    :param buttons: buttons need to be pressed, supports ``OneOfMouseButtons``, ``AnyMouseButton``
    """

    for button in buttons:
        if isinstance(button, AnyMouseButton):
            random_button: MagiqueMouseButton = random.choice(all_buttons)
            _press_and_release(random_button.button, hold_seconds)
            continue

        if isinstance(button, OneOfMouseButtons):
            random_button: MagiqueMouseButton = random.choice(button.buttons)
            _press_and_release(random_button.button, hold_seconds)
            continue

        _press_and_release(button.button)


_any_button_held: MagiqueMouseButton | None = None
_one_of_buttons_held: MagiqueMouseButton | None = None


def hold(*buttons: MagiqueMouseButton) -> None:
    """
    Presses and holds specified buttons by order
    :param buttons: buttons need to be held, supports ``OneOfMouseButtons``, ``AnyMouseButton``
    """

    for button in buttons:
        if isinstance(button, AnyMouseButton):
            global _any_button_held
            if _any_button_held is not None:
                continue

            random_button: MagiqueMouseButton = random.choice(all_buttons)
            _any_button_held = random_button
            mouse.press(random_button.button)
            continue

        if isinstance(button, OneOfMouseButtons):
            global _one_of_buttons_held
            if _one_of_buttons_held is not None:
                continue

            random_button: MagiqueMouseButton = random.choice(button.buttons)
            _one_of_buttons_held = random_button
            mouse.press(random_button.button)
            continue

        mouse.press(button.button)


def release(*buttons: MagiqueMouseButton) -> None:
    """
    Releases specified held buttons by order
    :param buttons: buttons need to be released, supports ``OneOfMouseButtons``, ``AnyMouseButton``
    """

    for button in buttons:
        if isinstance(button, AnyMouseButton):
            global _any_button_held
            if _any_button_held is None:
                continue

            mouse.release(_any_button_held.button)
            _any_button_held = None
            continue

        if isinstance(button, OneOfMouseButtons):
            global _one_of_buttons_held
            if _one_of_buttons_held is None:
                continue

            mouse.release(_one_of_buttons_held.button)
            _one_of_buttons_held = None
            continue

        mouse.release(button.button)


def double_press(*buttons: MagiqueMouseButton) -> None:
    press(*buttons)
    press(*buttons)


def press_combo(*buttons: MagiqueMouseButton) -> None:
    hold(*buttons)
    release(*reversed(buttons))
