import pytest

from typing import List
from src.magique.declarative import ObservableList


class TestContaining:
    def test_no_initialization(self):
        obs_list = ObservableList()
        assert obs_list.value == []

    @pytest.mark.parametrize("init_list", [[], [78.1], ["Hello", "World"], [1, 2, 3]])
    def test_initialization(self, init_list: List):
        obs_list = ObservableList(init_list)
        assert obs_list.value == init_list


class TestUpdateHandlers:
    def test_list_replaced(
            self,
            observable_list: ObservableList,
            target_list: List,
            list_adds_true_on_update):

        observable_list.value = [2]
        assert target_list == [True]

    def test_list_append(
            self,
            observable_list: ObservableList,
            target_list: List,
            list_adds_true_on_update):

        observable_list.append(5)
        observable_list.append(5)
        observable_list.append("Hello")
        assert target_list == [True, True, True]

    def test_list_update_by_index(
            self,
            observable_list: ObservableList,
            target_list: List,
            list_adds_true_on_update,
            initialize_list_by_numbers):

        observable_list[0] = 100
        observable_list[1] = 200

        assert target_list == [True, True]
        assert observable_list.value == [100, 200] + list(range(2, 10))

    def test_slicing(
            self,
            observable_list: ObservableList,
            target_list: List,
            list_adds_true_on_update,
            initialize_list_by_numbers):

        reversed_observable_list = observable_list[::-1]

        assert isinstance(reversed_observable_list, ObservableList)
        assert reversed_observable_list.value == list(reversed(range(0, 10)))

    def test_list_update_on_remove(
            self,
            observable_list: ObservableList,
            target_list: List,
            list_adds_true_on_update,
            initialize_list_by_numbers):

        observable_list.remove(5)
        observable_list.remove(0)
        observable_list.remove(9)

        assert target_list == [True, True, True]
        assert observable_list.value == list(range(1, 5)) + list(range(6, 9))

    def test_list_update_on_extend(
            self,
            observable_list: ObservableList,
            target_list: List,
            list_adds_true_on_update,
            initialize_list_by_numbers):

        tail: List = [25, 30, 35]
        observable_list.extend(tail)

        assert target_list == [True]
        assert observable_list.value == list(range(0, 10)) + tail

    def test_list_update_on_clear(
            self,
            observable_list: ObservableList,
            target_list: List,
            list_adds_true_on_update,
            initialize_list_by_numbers):

        observable_list.clear()

        assert target_list == [True]
        assert observable_list.value == []
