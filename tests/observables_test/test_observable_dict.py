import pytest

from typing import List, Dict
from src.magique.declarative import ObservableDict


class TestContaining:
    def test_no_initialization(self):
        obs_list = ObservableDict()
        assert obs_list.value == {}

    @pytest.mark.parametrize("init_dict", [{}, {5: 25}, {"abc": 32, "hey": "bruh"}])
    def test_initialization(self, init_dict: Dict):
        obs_list = ObservableDict(init_dict)
        assert obs_list.value == init_dict


class TestUpdateHandlers:
    def test_dict_replaced(
            self,
            observable_dict: ObservableDict,
            target_list: List,
            list_adds_true_on_dict_update):

        observable_dict.value = {"yes": "yes"}
        assert target_list == [True]

    def test_dict_update_by_index(
            self,
            observable_dict: ObservableDict,
            target_list: List,
            list_adds_true_on_dict_update):

        observable_dict["yes"] = "no"
        observable_dict[25] = 125
        observable_dict[789.11] = "hello"
        assert target_list == [True, True, True]

    def test_dict_update_on_delete(
            self,
            observable_dict: ObservableDict,
            target_list: List,
            list_adds_true_on_dict_update,
            initialize_dict_by_numbers):

        del observable_dict["0"]
        del observable_dict["5"]
        del observable_dict["9"]

        assert target_list == [True, True, True]
        assert observable_dict.value == {**{str(i): i for i in range(1, 5)}, **{str(i): i for i in range(6, 9)}}

    def test_list_update_on_update(
            self,
            observable_dict: ObservableDict,
            target_list: List,
            list_adds_true_on_dict_update,
            initialize_dict_by_numbers):

        tail: Dict = {25: 25, "yes": "nope"}
        observable_dict.update(tail)

        assert target_list == [True]
        assert observable_dict.value == {**{str(i): i for i in range(0, 10)}, **tail}

    def test_list_update_on_clear(
            self,
            observable_dict: ObservableDict,
            target_list: List,
            list_adds_true_on_dict_update,
            initialize_dict_by_numbers):

        observable_dict.clear()

        assert target_list == [True]
        assert observable_dict.value == {}
