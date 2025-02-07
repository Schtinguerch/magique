import pytest
from src.magique.declarative import Observable, Binding, BindingMode, Converter


class TestSingleReceiveBindingMode:
    def test_source_not_sends(
            self,
            observable_int: Observable[int],
            observable_str: Observable[str],
            int_str_converter: Converter):

        value_before_binding: str = observable_str.value
        binding = Binding(observable_int, observable_str, BindingMode.single_receive, int_str_converter)

        observable_int.value = 555
        assert observable_str.value == value_before_binding

    def test_destination_sends(
            self,
            observable_int: Observable[int],
            observable_str: Observable[str],
            int_str_converter: Converter):

        binding = Binding(observable_int, observable_str, BindingMode.single_receive, int_str_converter)
        value = "555"

        observable_str.value = value
        assert observable_int.value == int(value)

    def test_multiple_send(
            self,
            observable_int: Observable[int],
            observable_str: Observable[str],
            int_str_converter: Converter):

        values = ["1", "2", "3", "4", "5"]
        int_values = []

        binding = Binding(observable_int, observable_str, BindingMode.single_receive, int_str_converter)
        observable_int.attach_on_update(lambda v: int_values.append(v))

        for value in values:
            observable_str.value = value

        assert int_values == [int(values[0])]

    def test_instant_apply(
            self,
            observable_int: Observable[int],
            observable_str: Observable[str],
            int_str_converter: Converter):

        binding = Binding(observable_int, observable_str, BindingMode.single_receive, int_str_converter, True)
        assert observable_int.value == 500

    def test_not_apply_if_not_set(
            self,
            observable_int: Observable[int],
            observable_str: Observable[str],
            int_str_converter: Converter):

        str_value_before_binding: str = observable_str.value
        int_value_before_binding: int = observable_int.value

        binding = Binding(observable_int, observable_str, BindingMode.single_receive, int_str_converter)

        assert observable_str.value == str_value_before_binding
        assert observable_int.value == int_value_before_binding
