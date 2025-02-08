from math import sin, cos, pi, sqrt
from typing import Callable


def trigonometry_ease_func(
        trigonometry_func: Callable[[float], float],
        is_clockwise: bool = False,
        start_phase: float = 0.0) -> Callable[[float], float]:

    """
    Converts a trigonometry function to an ease function where x in [0;1]
    and y in [-1;1] for animations

    :param trigonometry_func: standard trigonometry function, to be mapped
    :param is_clockwise: value direction + or -, clockwise = +
    :param start_phase: start radian value, i.g. sin(x + start_phase)
    :return: trigonometry function, where x mapped to [0;1] for ease function limits
    """

    multiplier: int = -1 if is_clockwise else 1

    def ease_function(x: float) -> float:
        radian_value: float = x * 2 * pi
        return trigonometry_func(multiplier * radian_value + start_phase)

    return ease_function


def polynomial_ease_in_func(exp: float) -> Callable[[float], float]:
    """
    Creates an ease_in_function with specified exp value
    """

    def ease_in(x: float) -> float:
        return x ** exp

    return ease_in


def polynomial_ease_out_func(exp: float) -> Callable[[float], float]:
    """
    Creates an ease_out_function with specified exp value
    """

    def ease_out(x: float) -> float:
        return 1 - ((1 - x) ** exp)

    return ease_out


def polynomial_ease_in_out_func(exp: float) -> Callable[[float], float]:
    """
    Creates an ease_in_out_function with specified exp value
    """

    powered_two: float = 2 ** (exp - 1)

    def ease_in_out(x: float) -> float:
        return powered_two * (x ** exp) if x < 0.5 else 1 - ((-2 * x + 2) ** exp) / 2

    return ease_in_out


def linear(x: float) -> float:
    return x


def ease_in_sine(x: float) -> float:
    return 1 - cos((x * pi) / 2)


def ease_out_sine(x: float) -> float:
    return sin((x * pi) / 2)


def ease_in_out_sine(x: float) -> float:
    return -(cos(pi * x) - 1) / 2


def ease_in_quad(x: float) -> float:
    return x ** 2


def ease_out_quad(x: float) -> float:
    return 1 - ((1 - x) ** 2)


def ease_in_out_quad(x: float) -> float:
    return 2 * (x ** 2) if x < 0.5 else 1 - ((-2 * x + 2) ** 2) / 2


def ease_in_cubic(x: float) -> float:
    return x ** 3


def ease_out_cubic(x: float) -> float:
    return 1 - ((1 - x) ** 3)


def ease_in_out_cubic(x: float) -> float:
    return 4 * (x ** 3) if x < 0.5 else 1 - ((-2 * x + 2) ** 3) / 2


def ease_in_quart(x: float) -> float:
    return x ** 4


def ease_out_quart(x: float) -> float:
    return 1 - ((1 - x) ** 4)


def ease_in_out_quart(x: float) -> float:
    return 8 * (x ** 4) if x < 0.5 else 1 - ((-2 * x + 2) ** 4) / 2


def ease_in_quint(x: float) -> float:
    return x ** 5


def ease_out_quint(x: float) -> float:
    return 1 - ((1 - x) ** 5)


def ease_in_out_quint(x: float) -> float:
    return 16 * (x ** 5) if x < 0.5 else 1 - ((-2 * x + 2) ** 5) / 2


def ease_in_circ(x: float) -> float:
    return 1 - sqrt(1 - x ** 2)


def ease_out_circ(x: float) -> float:
    return sqrt(1 - (x - 1) ** 2)


def ease_in_out_circ(x: float) -> float:
    return (1 - sqrt(1 - (2 * x) ** 2)) / 2 if x < 0.5 else (sqrt(1 - ((-2 * x + 2) ** 2)) + 1) / 2


def ease_in_elastic(x: float) -> float:
    if x == 0: return 0
    if x == 1: return 1
    return -pow(2, 10 * x - 10) * sin((x * 10 - 10.75) * 2 * pi / 3)


def ease_out_elastic(x: float) -> float:
    if x == 0: return 0
    if x == 1: return 1
    return pow(2, -10 * x) * sin((x * 10 - 0.75) * 2 * pi / 3) + 1


def ease_in_out_elastic(x: float) -> float:
    if x == 0: return 0
    if x == 1: return 1

    if x < 0.5: return -(pow(2, 20 * x - 10) * sin((20 * x - 11.125) * 2 * pi / 4.5)) / 2
    return (pow(2, -20 * x + 10) * sin((20 * x - 11.125) * 2 * pi / 4.5)) / 2 + 1


def ease_in_expo(x: float) -> float:
    return 0 if x == 0 else 2 ** (10 * x - 10)


def ease_out_expo(x: float) -> float:
    return 1 if x == 1 else 1 - 2 ** (-10 * x)


def ease_in_out_expo(x: float) -> float:
    if x == 0: return 0
    if x == 1: return 1

    if x < 0.5: return (2 ** (20 * x - 10)) / 2
    return (2 - (2 ** (-20 * x + 10))) / 2


def ease_in_back(x: float) -> float:
    a: float = 1.70158
    return (a + 1) * (x ** 3) - (a * x ** 2)


def ease_out_back(x: float) -> float:
    a: float = 1.70158
    return 1 + (a + 1) * pow(x - 1, 3) + a * pow(x - 1, 2)


def ease_in_out_back(x: float) -> float:
    a: float = 1.70158
    if x < 0.5: return (((2 * x) ** 2) * (((a + 1) + 1) * 2 * x - (a + 1))) / 2
    return (((2 * x - 2) ** 2) * (((a + 1) + 1) * (x * 2 - 2) + (a + 1)) + 2) / 2
