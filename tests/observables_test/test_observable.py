import pytest

from typing import List
from src.magique.declarative import Observable


class TestContaining:
    def test_initialization(self):
        value: str = "Hello, world"
        observable: Observable[str] = Observable(value)
        assert value == observable.value

    def test_post_initialization(self):
        value: int = 256
        observable: Observable[int] = Observable()
        assert observable.value is None

        observable.value = value
        assert value == observable.value


class TestUpdateHandlers:
    @pytest.mark.parametrize("value,expected_list", [(25, [25]), (100, [])])
    def test_new_value_update(
            self,
            observable_int: Observable[int],
            target_list: List,
            value: int,
            expected_list: List):

        def increment_list(sender: int) -> None:
            target_list.append(sender)

        observable_int.attach_on_update(increment_list)
        observable_int.value = value
        assert target_list == expected_list

    @pytest.mark.parametrize("values,expected_list", [
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([5, 5, 5, 3, 3], [5, 3])
    ])
    def test_multiple_updates(
            self,
            observable_int: Observable[int],
            target_list: List,
            values: List[int],
            expected_list: List):

        def increment_list(sender: int) -> None:
            target_list.append(sender)

        observable_int.attach_on_update(increment_list)
        for value in values:
            observable_int.value = value

        assert target_list == expected_list

    def test_multiple_handlers(self, observable_int: Observable[int], target_list: List):
        def increment_list(sender: int) -> None:
            target_list.append(sender)

        def multiply_list(sender: int) -> None:
            for i, v in enumerate(target_list):
                target_list[i] = target_list[i] * sender

        observable_int.attach_on_update(increment_list)
        observable_int.attach_on_update(multiply_list)

        observable_int.value = 12  # [12] -> [144]
        observable_int.value = 6   # [144, 6] -> [864, 36]

        assert target_list == [864, 36]
