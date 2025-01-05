import pytest
from typing import List, Callable, Any
from src.magique.declarative import Observable, ObservableList


@pytest.fixture()
def observable_int() -> Observable[int]:
    observable: Observable[int] = Observable(100)
    yield observable
    observable.detach_all_handlers()


@pytest.fixture()
def target_list() -> List:
    return []


@pytest.fixture()
def append_to_target_list(target_list: List) -> Callable[[Any], Any]:
    return lambda x: target_list.append(x)


@pytest.fixture()
def append_true_to_target_list(target_list: List) -> Callable[[Any], Any]:
    return lambda x: target_list.append(True)


@pytest.fixture()
def list_adds_true_on_update(
        observable_list: ObservableList,
        append_true_to_target_list) -> ObservableList:

    observable_list.attach_on_update(append_true_to_target_list)
    return observable_list


@pytest.fixture()
def observable_list() -> ObservableList:
    observable = ObservableList()
    yield observable
    observable.detach_all_handlers()


@pytest.fixture()
def initialize_list_by_numbers(observable_list: ObservableList) -> None:
    numbers: List[int] = list(range(0, 10))
    observable_list.no_event_set_value(numbers)
