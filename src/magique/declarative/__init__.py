"""
This module contains classes and functions for
reactive programming, creating hooks, etc.

Most of builtin components in magique is
based on following classes
"""


from .notify_updated import NotifyUpdated, notify_property_updated
from .observable import Observable, obs
from .observable_list import ObservableList, olist, ol
from .observable_dict import ObservableDict, odict, od
from .loop_metrics import LoopMetrics, loop_obs
from .hook_metrics import HookMetrics, hook_obs

from .when_condition import WhenCondition
from .when_functions import when
