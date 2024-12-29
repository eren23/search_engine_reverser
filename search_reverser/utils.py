import time
from typing import Callable, Any


def measure_timing(func: Callable) -> float:
    """Measure the execution time of a function"""
    start_time = time.time()
    func()
    return time.time() - start_time
