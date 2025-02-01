from typing import List, Dict, Self, Tuple
from ...declarative import NotifyUpdated
import sys
import keyboard


class MagiqueKey(NotifyUpdated):
    def __init__(self, pyautogui_string: str, canonical_string: str):
        super().__init__()
        self.pyguiauto_string: str = pyautogui_string
        self.canonical_string: str = canonical_string

    def is_pressed(self) -> bool:
        return keyboard.is_pressed(self.canonical_string)
    
    def is_released(self) -> bool:
        return not keyboard.is_pressed(self.canonical_string)


class CrossPlatformKey(MagiqueKey):
    def __init__(self, win_or_linux_key: MagiqueKey, macos_key: MagiqueKey):
        initializer: MagiqueKey = macos_key if sys.platform == "darwin" else win_or_linux_key
        super().__init__(initializer.pyguiauto_string, initializer.canonical_string)


class AnyKey(MagiqueKey):
    def __init__(self):
        super().__init__("", "")
        self.pressed: bool = False

    def is_pressed(self) -> bool:
        return self.pressed

    def is_released(self) -> bool:
        return not self.pressed


class OneOfKeys(MagiqueKey):
    redirect_dict: Dict[MagiqueKey, List[Self]] = {}

    # noinspection PyTypeChecker
    def __init__(self, *keys: MagiqueKey):
        super().__init__("", "")
        self.keys: Tuple[MagiqueKey] = keys

        for key in self.keys:
            if key in self.redirect_dict:
                self.redirect_dict[key].append(self)
            else:
                self.redirect_dict[key] = [self]

    def is_pressed(self) -> bool:
        return any(map(lambda k: k.is_pressed(), self.keys))

    def is_released(self) -> bool:
        return all(map(lambda k: k.is_released(), self.keys))

