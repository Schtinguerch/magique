from typing import Tuple, Dict, Type
from .notify_updated import NotifyUpdated, notify_property_updated


def add_property(cls, self, attribute: str, source: Tuple | Dict | None = None):
    private_attribute: str = f"_{attribute}"

    def get_attribute(self):
        return getattr(self, private_attribute)

    @notify_property_updated(get_attribute, attribute)
    def set_attribute(self, new_value):
        setattr(self, private_attribute, new_value)

    init_value = getattr(cls, attribute) if source is None else None
    setattr(cls, attribute, property(get_attribute, set_attribute))

    if isinstance(source, Dict):
        kwargs: Dict = source
        setattr(self, private_attribute, kwargs[attribute])
    elif isinstance(source, Tuple):
        args: Tuple = source
        setattr(self, private_attribute, args[0])
    else:
        setattr(self, private_attribute, init_value)


def notify_property_dataclass(cls):
    cls_annotations: Dict[str, Type] = cls.__annotations__
    if cls.__mro__[1] != NotifyUpdated:
        cls = type(cls.__name__, (NotifyUpdated,), dict(cls.__dict__))

    def __init__(self, *args, **kwargs):
        NotifyUpdated.__init__(self)

        for attribute in cls_annotations.keys():
            if len(args) > 0:
                add_property(cls, self, attribute, args)
                args = args[1:]

            elif attribute in kwargs:
                add_property(cls, self, attribute, kwargs)

            else:
                add_property(cls, self, attribute)

    def item_repr(self) -> str:
        properties_str = (f"{attr}={getattr(self, attr).__repr__()}" for attr in cls_annotations.keys())
        return f"<{cls.__name__} as {notify_property_dataclass.__name__}: {'; '.join(properties_str)}>"

    cls.__init__ = __init__
    cls.__repr__ = item_repr
    cls.__str__ = item_repr
    return cls
