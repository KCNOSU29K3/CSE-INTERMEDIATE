#!/usr/bin/env python3

from time import perf_counter_ns

def timed(function):
    """
    Returns the value of a function and the time it took to run in nanoseconds.
    """
    

    def wrapper(*args, **kwargs):
        # grabs the performance time in NS

        start = perf_counter_ns()
        i = function(*args, **kwargs)
        end = perf_counter_ns()
        ns = end - start
        s = ns/1000000000
        return i, ns, s

    return wrapper



