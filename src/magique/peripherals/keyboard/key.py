#from ....magique.declarative import Observable
import sys
import keyboard


class MagiqueKey:
    def __init__(self, pyautogui_string: str, canonical_string: str):
        self.pyguiauto_string: str = pyautogui_string
        self.canonical_string: str = canonical_string

    def is_pressed(self) -> bool:
        return keyboard.is_pressed(self.canonical_string)


class CrossPlatformKey(MagiqueKey):
    def __init__(self, win_or_linux_key: MagiqueKey, macos_key: MagiqueKey):
        initializer: MagiqueKey = macos_key if sys.platform == "darwin" else win_or_linux_key
        super().__init__(initializer.pyguiauto_string, initializer.canonical_string)
