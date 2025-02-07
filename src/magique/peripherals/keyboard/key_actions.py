import keyboard
import random
import time

from .key import MagiqueKey, AnyKey, OneOfKeys
from .keys import all_keys


def _press_and_release(canonical_string: str, hold_seconds: float | None = None) -> None:
    keyboard.press(canonical_string)
    if hold_seconds is not None: time.sleep(hold_seconds)
    keyboard.release(canonical_string)


def press(*keys: MagiqueKey, hold_seconds: float | None = None) -> None:
    """
    Presses and releases specified keys by order (not a hotkey)
    :param hold_seconds: time to hold the key pressed, by default release is done immediately
    :param keys: keys need to be pressed, supports ``OneOfKeys``, ``AnyKey``, ``CrossPlatformKey``
    """

    for key in keys:
        if isinstance(key, AnyKey):
            random_key: MagiqueKey = random.choice(all_keys)
            _press_and_release(random_key.canonical_string, hold_seconds)
            continue

        if isinstance(key, OneOfKeys):
            random_key: MagiqueKey = random.choice(key.keys)
            _press_and_release(random_key.canonical_string, hold_seconds)
            continue

        _press_and_release(key.canonical_string)


_any_key_held: MagiqueKey | None = None
_one_of_keys_held: MagiqueKey | None = None


def hold(*keys: MagiqueKey) -> None:
    """
    Presses and holds specified keys by order
    :param keys: keys need to be held, supports ``OneOfKeys``, ``AnyKey``, ``CrossPlatformKey``
    """

    for key in keys:
        if isinstance(key, AnyKey):
            global _any_key_held
            if _any_key_held is not None:
                continue

            random_key: MagiqueKey = random.choice(all_keys)
            _any_key_held = random_key
            keyboard.press(random_key.canonical_string)
            continue

        if isinstance(key, OneOfKeys):
            global _one_of_keys_held
            if _one_of_keys_held is not None:
                continue

            random_key: MagiqueKey = random.choice(key.keys)
            _one_of_keys_held = random_key
            keyboard.press(random_key.canonical_string)
            continue

        keyboard.press(key.canonical_string)


def release(*keys: MagiqueKey) -> None:
    """
    Releases specified held keys by order
    :param keys: keys need to be released, supports ``OneOfKeys``, ``AnyKey``, ``CrossPlatformKey``
    """

    for key in keys:
        if isinstance(key, AnyKey):
            global _any_key_held
            if _any_key_held is None:
                continue

            keyboard.release(_any_key_held.canonical_string)
            _any_key_held = None
            continue

        if isinstance(key, OneOfKeys):
            global _one_of_keys_held
            if _one_of_keys_held is None:
                continue

            keyboard.release(_one_of_keys_held.canonical_string)
            _one_of_keys_held = None
            continue

        keyboard.release(key.canonical_string)


def double_press(*keys: MagiqueKey) -> None:
    press(*keys)
    press(*keys)


def press_hotkey(*keys: MagiqueKey) -> None:
    hold(*keys)
    release(*reversed(keys))
