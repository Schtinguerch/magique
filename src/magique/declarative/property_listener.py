from typing import TypeVar, Any
from .notify_updated import NotifyUpdated
from .observable import Observable
from .observable_receiver import ObservableReceiver


T = TypeVar('T')


class PropertyListener(Observable[T]):
    """
    A special proxy for object's property, like an observable gateway
    raising updates when the property updates and updates the property
    when its value or receiver's value us updated

    It contains two instances inside:
     - ``property_updated`` is ``NotifyUpdated`` instance
     - ``property_received`` is ``ObservableReceiver`` instance
    """

    def __init__(
            self,
            property_updated: NotifyUpdated,
            property_received: ObservableReceiver):

        super().__init__(property_received.value)
        self._property_updated: NotifyUpdated = property_updated
        self._property_received: ObservableReceiver = property_received

        self._subscribe_updated(self._property_updated)
        self._subscribe_received(self._property_received)

    @property
    def property_updated_instance(self) -> NotifyUpdated:
        return self._property_updated

    @property_updated_instance.setter
    def property_updated_instance(self, new_instance: NotifyUpdated):
        self._unsubscribe_updated(self._property_updated)
        self._property_updated = new_instance
        self._subscribe_updated(self._property_updated)

    @property
    def property_received_instance(self) -> ObservableReceiver:
        return self._property_received

    @property_received_instance.setter
    def property_received_instance(self, new_instance: ObservableReceiver):
        self._unsubscribe_received(self._property_received)
        self._property_received = new_instance
        self._subscribe_received(self._property_received)

    @Observable.value.setter
    def value(self, new_value: T):
        if new_value == self._value:
            return

        self._value = new_value
        self._property_received.value = new_value
        self.raise_update_event()

    def _subscribe_updated(self, property_updated: NotifyUpdated):
        property_updated.attach_on_update(self._property_updated_handler)

    def _unsubscribe_updated(self, property_updated: NotifyUpdated):
        property_updated.detach_on_update(self._property_updated_handler)

    def _subscribe_received(self, property_received: ObservableReceiver):
        property_received.attach_on_update(self._property_received_handler)

    def _unsubscribe_received(self, property_received: ObservableReceiver):
        property_received.detach_on_update(self._property_received_handler)

    def _property_updated_handler(self, notifier: NotifyUpdated) -> None:
        # to avoid double raise event
        if self._value == notifier.value:
            return

        self._value = notifier.value
        self.raise_update_event()

    def _property_received_handler(self, value: Any) -> None:
        self.value = value
