import pytest
from src.magique.declarative import Observable, Binding, BindingMode, Converter


class TestSendBindingMode:
    def test_source_sends(
            self,
            observable_int: Observable[int],
            observable_str: Observable[str],
            int_str_converter: Converter):

        binding = Binding(observable_int, observable_str, BindingMode.send, int_str_converter)
        value = 555

        observable_int.value = value
        assert observable_str.value == str(value)

    def test_destination_not_sends(
            self,
            observable_int: Observable[int],
            observable_str: Observable[str],
            int_str_converter: Converter):

        value_before: int = observable_int.value
        binding = Binding(observable_int, observable_str, BindingMode.send, int_str_converter)

        observable_str.value = 555
        assert observable_int.value == value_before

    def test_multiple_send(
            self,
            observable_int: Observable[int],
            observable_str: Observable[str],
            int_str_converter: Converter):

        values = [1, 2, 3, 4, 5]
        str_values = []

        binding = Binding(observable_int, observable_str, BindingMode.send, int_str_converter)
        observable_str.attach_on_update(lambda v: str_values.append(v))

        for value in values:
            observable_int.value = value

        assert str_values == [str(value) for value in values]

    def test_instant_apply(
            self,
            observable_int: Observable[int],
            observable_str: Observable[str],
            int_str_converter: Converter):

        binding = Binding(observable_int, observable_str, BindingMode.send, int_str_converter, True)
        assert observable_str.value == "100"

    def test_not_apply_if_not_set(
            self,
            observable_int: Observable[int],
            observable_str: Observable[str],
            int_str_converter: Converter):

        str_value_before_binding: str = observable_str.value
        int_value_before_binding: int = observable_int.value

        binding = Binding(observable_int, observable_str, BindingMode.send, int_str_converter)

        assert observable_str.value == str_value_before_binding
        assert observable_int.value == int_value_before_binding
