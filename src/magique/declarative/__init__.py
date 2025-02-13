"""
This module contains classes and functions for
reactive programming, creating hooks, etc.

Most of builtin components in magique is
based on following classes
"""


from .notify_updated import NotifyUpdated, notify_property_updated
from .notify_properties_dataclass import notify_property_dataclass
from .observable import Observable, obs
from .observable_receiver import ObservableReceiver
from .property_listener import PropertyListener
from .binding import Binding, BindingMode, Converter, FunctionPair
from .observable_list import ObservableList, olist, ol
from .observable_dict import ObservableDict, odict, od
from .loop_metrics import LoopMetrics, loop_obs, loop_metrics
from .hook_metrics import HookMetrics, hook_obs, hook_metrics

from .when_condition import WhenCondition
from .selective_when import SelectiveWhenCondition, selective_when
from .when_functions import when, invoke_when, with_observables
