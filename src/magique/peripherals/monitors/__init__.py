from typing import Final, List
from screeninfo import get_monitors, Monitor
from .monitor_info import MonitorSetup, MonitorInfo


monitor_setup: Final[MonitorSetup] = MonitorSetup()


def auto_init_monitor_setup() -> None:
    monitors_info: List[Monitor] = get_monitors()
    monitor_setup.reinit(monitors_info)


def manual_init_monitor_setup(monitors_info: List[MonitorInfo]) -> None:
    monitor_setup.monitors.no_event_set_value(monitors_info)
