from typing import List, Any, Literal
from . import MagiqueKey, OneOfKeys, str_key_dict, Any

from keyboard import hook, KeyboardEvent


now_pressed_keys: List[MagiqueKey] = []


def on_any_key(event: KeyboardEvent) -> None:
    key_action: Literal["down", "up"] | None = event.event_type

    if event.name in str_key_dict:
        key: MagiqueKey = str_key_dict[event.name]
        key.raise_update_event()

        if key in OneOfKeys.redirect_dict:
            for dir_key in OneOfKeys.redirect_dict[key]:
                dir_key.raise_update_event()

    Any.pressed = key_action == "down"
    Any.raise_update_event()


hook(on_any_key)
