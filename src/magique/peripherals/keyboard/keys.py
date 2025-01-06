from typing import Final
from .key import MagiqueKey, CrossPlatformKey


LeftCtrl: Final[MagiqueKey] = MagiqueKey("lctrl", "left ctrl")
RightCtrl: Final[MagiqueKey] = MagiqueKey("rctrl", "right ctrl")
Ctrl: Final[MagiqueKey] = LeftCtrl

Control: Final[MagiqueKey] = MagiqueKey("ctrl", "ctrl")
Command: Final[MagiqueKey] = MagiqueKey("command", "command")
Option: Final[MagiqueKey] = MagiqueKey("option", "alt")

LeftShift: Final[MagiqueKey] = MagiqueKey("lshift", "left shift")
RightShift: Final[MagiqueKey] = MagiqueKey("rshift", "right shift")
Shift: Final[MagiqueKey] = LeftShift

LeftWin: Final[MagiqueKey] = MagiqueKey("lwin", "left windows")
RightWin: Final[MagiqueKey] = MagiqueKey("rwin", "right windows")
Win: Final[MagiqueKey] = LeftWin

LeftAlt: Final[MagiqueKey] = MagiqueKey("alt", "left alt")
RightAlt: Final[MagiqueKey] = MagiqueKey("altright", "alt gr")
Alt: Final[MagiqueKey] = LeftAlt
AltGr: Final[MagiqueKey] = RightAlt

CapsLock: Final[MagiqueKey] = MagiqueKey("capslock", "caps lock")
Caps: Final[MagiqueKey] = CapsLock

Enter: Final[MagiqueKey] = MagiqueKey("enter", "enter")
Return: Final[MagiqueKey] = Enter

Tab: Final[MagiqueKey] = MagiqueKey("tab", "tab")
Backspace: Final[MagiqueKey] = MagiqueKey("backspace", "backspace")
Delete: Final[MagiqueKey] = MagiqueKey("delete", "delete")
Escape: Final[MagiqueKey] = MagiqueKey("esc", "esc")
Esc: Final[MagiqueKey] = Escape


F1: Final[MagiqueKey] = MagiqueKey("f1", "f1")
F2: Final[MagiqueKey] = MagiqueKey("f2", "f2")
F3: Final[MagiqueKey] = MagiqueKey("f3", "f3")
F4: Final[MagiqueKey] = MagiqueKey("f4", "f4")
F5: Final[MagiqueKey] = MagiqueKey("f5", "f5")
F6: Final[MagiqueKey] = MagiqueKey("f6", "f6")
F7: Final[MagiqueKey] = MagiqueKey("f7", "f7")
F8: Final[MagiqueKey] = MagiqueKey("f8", "f8")
F9: Final[MagiqueKey] = MagiqueKey("f9", "f9")
F10: Final[MagiqueKey] = MagiqueKey("f9", "f10")
F11: Final[MagiqueKey] = MagiqueKey("f11", "f11")
F12: Final[MagiqueKey] = MagiqueKey("f12", "f12")
F13: Final[MagiqueKey] = MagiqueKey("f13", "f13")
F14: Final[MagiqueKey] = MagiqueKey("f14", "f14")
F15: Final[MagiqueKey] = MagiqueKey("f15", "f15")
F16: Final[MagiqueKey] = MagiqueKey("f16", "f16")
F17: Final[MagiqueKey] = MagiqueKey("f17", "f17")
F18: Final[MagiqueKey] = MagiqueKey("f18", "f18")
F19: Final[MagiqueKey] = MagiqueKey("f19", "f19")
F20: Final[MagiqueKey] = MagiqueKey("f20", "f20")
F21: Final[MagiqueKey] = MagiqueKey("f21", "f21")
F22: Final[MagiqueKey] = MagiqueKey("f22", "f22")
F23: Final[MagiqueKey] = MagiqueKey("f23", "f23")
F24: Final[MagiqueKey] = MagiqueKey("f24", "f24")


Home: Final[MagiqueKey] = MagiqueKey("home", "home")
PageUp: Final[MagiqueKey] = MagiqueKey("pageup", "page up")
PageDown: Final[MagiqueKey] = MagiqueKey("pagedown", "page down")
End: Final[MagiqueKey] = MagiqueKey("end", "end")
PrintScreen: Final[MagiqueKey] = MagiqueKey("printscreen", "print screen")
Insert: Final[MagiqueKey] = MagiqueKey("insert", "insert")
Space: Final[MagiqueKey] = MagiqueKey("space", "space")

PgUp: Final[MagiqueKey] = PageUp
PgDn: Final[MagiqueKey] = PageDown
PrtSc: Final[MagiqueKey] = PrintScreen
Ins: Final[MagiqueKey] = Insert


D0: Final[MagiqueKey] = MagiqueKey("0", "0")
D1: Final[MagiqueKey] = MagiqueKey("1", "1")
D2: Final[MagiqueKey] = MagiqueKey("2", "2")
D3: Final[MagiqueKey] = MagiqueKey("3", "3")
D4: Final[MagiqueKey] = MagiqueKey("4", "4")
D5: Final[MagiqueKey] = MagiqueKey("5", "5")
D6: Final[MagiqueKey] = MagiqueKey("6", "6")
D7: Final[MagiqueKey] = MagiqueKey("7", "7")
D8: Final[MagiqueKey] = MagiqueKey("8", "8")
D9: Final[MagiqueKey] = MagiqueKey("9", "9")

Zero: Final[MagiqueKey] = D0
One: Final[MagiqueKey] = D1
Two: Final[MagiqueKey] = D2
Three: Final[MagiqueKey] = D3
Four: Final[MagiqueKey] = D4
Five: Final[MagiqueKey] = D5
Six: Final[MagiqueKey] = D6
Seven: Final[MagiqueKey] = D7
Eight: Final[MagiqueKey] = D8
Nine: Final[MagiqueKey] = D9


Tilde: Final[MagiqueKey] = MagiqueKey("~", "~")
Grave: Final[MagiqueKey] = MagiqueKey("`", "`")
Minus: Final[MagiqueKey] = MagiqueKey("-", "-")
Equal: Final[MagiqueKey] = MagiqueKey("=", "=")


Q: Final[MagiqueKey] = MagiqueKey("q", "q")
W: Final[MagiqueKey] = MagiqueKey("w", "w")
E: Final[MagiqueKey] = MagiqueKey("e", "e")
R: Final[MagiqueKey] = MagiqueKey("r", "r")
T: Final[MagiqueKey] = MagiqueKey("t", "t")
Y: Final[MagiqueKey] = MagiqueKey("y", "y")
U: Final[MagiqueKey] = MagiqueKey("u", "u")
I: Final[MagiqueKey] = MagiqueKey("i", "i")
O: Final[MagiqueKey] = MagiqueKey("o", "o")
P: Final[MagiqueKey] = MagiqueKey("p", "p")

A: Final[MagiqueKey] = MagiqueKey("a", "a")
S: Final[MagiqueKey] = MagiqueKey("s", "s")
D: Final[MagiqueKey] = MagiqueKey("d", "d")
F: Final[MagiqueKey] = MagiqueKey("f", "f")
G: Final[MagiqueKey] = MagiqueKey("g", "g")
H: Final[MagiqueKey] = MagiqueKey("h", "h")
J: Final[MagiqueKey] = MagiqueKey("j", "j")
K: Final[MagiqueKey] = MagiqueKey("k", "k")
L: Final[MagiqueKey] = MagiqueKey("l", "l")

Z: Final[MagiqueKey] = MagiqueKey("z", "z")
X: Final[MagiqueKey] = MagiqueKey("x", "x")
C: Final[MagiqueKey] = MagiqueKey("c", "c")
V: Final[MagiqueKey] = MagiqueKey("v", "v")
B: Final[MagiqueKey] = MagiqueKey("b", "b")
N: Final[MagiqueKey] = MagiqueKey("n", "n")
M: Final[MagiqueKey] = MagiqueKey("m", "m")

BracketLeft: Final[MagiqueKey] = MagiqueKey("[", "[")
BracketRight: Final[MagiqueKey] = MagiqueKey("]", "]")
BraceLeft: Final[MagiqueKey] = MagiqueKey("{", "{")
BraceRight: Final[MagiqueKey] = MagiqueKey("}", "}")
Backslash: Final[MagiqueKey] = MagiqueKey("\\", "\\")
Semicolon: Final[MagiqueKey] = MagiqueKey(";", ";")
Apostrophe: Final[MagiqueKey] = MagiqueKey("'", "'")
Comma: Final[MagiqueKey] = MagiqueKey(",", ",")
Period: Final[MagiqueKey] = MagiqueKey(".", ".")
Slash: Final[MagiqueKey] = MagiqueKey("/", "/")


NumLock: Final[MagiqueKey] = MagiqueKey("numlock", "num lock")
ScrollLock: Final[MagiqueKey] = MagiqueKey("scrolllock", "scroll lock")


PlayPause: Final[MagiqueKey] = MagiqueKey("playpause", "play/pause media")
Previous: Final[MagiqueKey] = MagiqueKey("prevtrack", "prior")
Next: Final[MagiqueKey] = MagiqueKey("nexttrack", "next")


#  MacOS equivalents for Win/Linux keys for cross-platform scripts
#  Most of cross-platform apps supporting macOS, has that equivalent
#  for keyboard hotkeys: Ctrl+A -> Command+A, Ctrl+Alt+X -> Command+Option+X

BackspaceOrDelete: Final[CrossPlatformKey] = CrossPlatformKey(Backspace, Delete)
CtrlOrCommand: Final[CrossPlatformKey] = CrossPlatformKey(Ctrl, Command)
AltOrOption: Final[CrossPlatformKey] = CrossPlatformKey(Alt, Option)
AltGrOrOption: Final[CrossPlatformKey] = CrossPlatformKey(AltGr, Option)
