from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any, Tuple

from .notify_updated import NotifyUpdated, notify_property_updated


FunctionPair = Tuple[Callable[[Any], Any], Callable[[Any], Any]]
_sentinel: Any = object()


@dataclass
class Converter:
    """
    A special function pair for ``Binding`` value converting
     - ``convert`` - function to convert from ``source`` to ``destination``
     - ``convert_back`` - function to convert from ``destination`` to ``source``
    """

    convert: Callable[[Any], Any]
    convert_back: Callable[[Any], Any]


class BindingMode(Enum):
    """
    Enum to set up the mode of binding two observables
     - ``send`` - ``source`` updates ``destination``
     - ``receive`` - ``destination`` updates ``source``
     - ``two_way`` - both from send and receive, has a way to prevent double updates and looping
     - ``single_send`` - ``source`` updates ``destination`` only one time
     - ``single_receive`` - ``destination`` updates ``source`` only one time
    """

    send = "send"
    """Mode when ``source`` update triggers ``destination`` update"""

    receive = "receive"
    """Mode when ``destination`` update triggers ``source`` update"""

    two_way = "two_way"
    """
    Mode with two way updates, as both ``send`` and ``receive`` modes
    
    The mode prevents double updates, endless loops and other 
    unpredictable updates by-design
    """

    single_send = "single_send"
    """Mode when ``source`` update triggers ``destination`` update **only once**"""

    single_receive = "single_receive"
    """Mode when ``destination`` update triggers ``source`` update **only once**"""


class Binding(NotifyUpdated):
    """
    The object allows automatically bind values updates between
    two ``NotifyUpdated`` instances with additional parameters
     - ``mode`` - one of binding modes setting the updating way
     - ``converters`` - the 2 functions for direct and reversed value converting
     - ``apply_immediately`` - raise update event manually after init
    """

    def __init__(
            self,
            source: NotifyUpdated,
            destination: NotifyUpdated,
            mode: BindingMode = BindingMode.send,
            converter: Converter | FunctionPair = _sentinel,
            apply_immediately: bool = False):

        super().__init__()
        self._first_update_done: bool = False

        self._source: NotifyUpdated = source
        self._destination: NotifyUpdated = destination
        self._mode: BindingMode = mode
        self._enable_mode(mode)

        if converter is _sentinel:
            self.converter = Converter(lambda x: x, lambda x: x)
        elif isinstance(converter, Tuple):
            self.converter = Converter(*converter)
        else:
            self.converter: Converter = converter

        if apply_immediately:
            if self.mode in {BindingMode.send, BindingMode.single_send, BindingMode.two_way}:
                source.raise_update_event()
            elif self.mode in {BindingMode.receive, BindingMode.single_receive}:
                destination.raise_update_event()

    def __repr__(self) -> str:
        return (
            f"<binding: mode={self._mode.name}; "
            f"between {self._source.__repr__()} AND {self._destination.__repr__()}>"
        )

    def __str__(self) -> str:
        return f"binding(mode={self._mode.name})"

    @property
    def source(self) -> NotifyUpdated: return self._source

    @source.setter
    @notify_property_updated(lambda self: self._source)
    def source(self, new_obs: NotifyUpdated):
        self._disable_mode(self.mode)
        self._source = new_obs
        self._enable_mode(self.mode)

    @property
    def destination(self) -> NotifyUpdated: return self._destination

    @destination.setter
    @notify_property_updated(lambda self: self._destination)
    def destination(self, new_obs: NotifyUpdated):
        self._disable_mode(self.mode)
        self._destination = new_obs
        self._enable_mode(self.mode)

    @property
    def mode(self) -> BindingMode: return self._mode

    @mode.setter
    @notify_property_updated(lambda self: self._mode)
    def mode(self, new_mode: BindingMode):
        self._disable_mode(self.mode)
        self._enable_mode(new_mode)
        self._mode = new_mode

    def _disable_mode(self, mode: BindingMode) -> None:
        if mode == BindingMode.send:
            self.source.detach_on_update(self._update_destination_from_source)
        elif mode == BindingMode.receive:
            self.destination.detach_on_update(self._update_source_from_destination)
        elif mode == BindingMode.two_way:
            self.source.detach_on_update(self._update_destination_from_source)
            self.destination.detach_on_update(self._update_source_from_destination)
        elif mode == BindingMode.single_send:
            self.source.detach_on_update(self._one_time_update_destination_from_source)
        elif mode == BindingMode.single_receive:
            self.destination.detach_on_update(self._one_time_update_source_from_destination)

    def _enable_mode(self, mode: BindingMode) -> None:
        if mode == BindingMode.send:
            self.source.attach_on_update(self._update_destination_from_source)
        elif mode == BindingMode.receive:
            self.destination.attach_on_update(self._update_source_from_destination)
        elif mode == BindingMode.two_way:
            self.source.attach_on_update(self._update_destination_from_source)
            self.destination.attach_on_update(self._update_source_from_destination)
        elif mode == BindingMode.single_send:
            self._first_update_done = False
            self.source.attach_on_update(self._one_time_update_destination_from_source)
        elif mode == BindingMode.single_receive:
            self._first_update_done = False
            self.destination.attach_on_update(self._one_time_update_source_from_destination)

    def _update_destination_from_source(self, new_value: Any) -> None:
        if self.destination.is_sending: return
        if isinstance(new_value, NotifyUpdated):
            new_value = new_value.value

        self.source.is_sending = True
        self.destination.value = self.converter.convert(new_value)
        self.source.is_sending = False

    def _update_source_from_destination(self, new_value: Any) -> None:
        if self.source.is_sending: return
        if isinstance(new_value, NotifyUpdated):
            new_value = new_value.value

        self.destination.is_sending = True
        self.source.value = self.converter.convert_back(new_value)
        self.destination.is_sending = False

    def _one_time_update_destination_from_source(self, new_value: Any) -> None:
        if self._first_update_done: return
        self._first_update_done = True
        self._update_destination_from_source(new_value)

    def _one_time_update_source_from_destination(self, new_value: Any) -> None:
        if self._first_update_done: return
        self._first_update_done = True
        self._update_source_from_destination(new_value)
