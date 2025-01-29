from typing import Final, List
from screeninfo import get_monitors, Monitor

from .monitor_info import MonitorSetup, MonitorInfo
from ....magique.declarative import LoopMetrics


monitor_setup: Final[MonitorSetup] = MonitorSetup()


def auto_init_monitor_setup() -> None:
    monitors_info: List[Monitor] = get_monitors()
    monitor_setup.reinit(monitors_info)


def check_monitor_setup() -> None:
    monitors_info: List[Monitor] = get_monitors()
    monitor_setup.update(monitors_info)


monitor_checkout_loop = LoopMetrics(check_monitor_setup, loop_delay_seconds=1)
#monitor_checkout_loop.start_metrics_loop()
