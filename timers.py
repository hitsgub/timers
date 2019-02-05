from functools import wraps
import inspect
import os
import pathlib
import time


# Select the best-resolution timer function
try:
    _get_time = time.perf_counter
except AttributeError:
    if os.name == 'nt':
        _get_time = time.clock
    else:
        _get_time = time.time


def location():
    """Returns a location of running code."""
    frame = inspect.stack()[1][0]
    info = inspect.getframeinfo(frame)
    fname = pathlib.Path(info.filename).name
    return '{}(L{})'.format(fname, info.lineno)


def _humanized_time(second, precision=3):
    """Returns a human readable time."""
    form = '.{}f%s'.format(precision)
    for unit in ['sec', 'ms', 'us']:
        if second >= 1:
            return ('%3' + form) % (second, unit)
        second *= 1000.0
    return ('%' + form) % (second, 'ns')


def timer(precision=3):
    def _decorator(func):
        @wraps(func)
        def _decorated(*args, **kargs):
            start = _get_time()
            result = func(*args, **kargs)
            proc_time = _get_time() - start
            str_time = _humanized_time(proc_time, precision)
            print('{}: {}'.format(func.__name__, str_time))
            return result
        return _decorated
    return _decorator


class Timer(object):
    def __init__(self, precision=3):
        self.precision = precision

    def __enter__(self):
        self.start = _get_time()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        proc_time = _get_time() - self.start
        str_time = _humanized_time(proc_time, self.precision)
        print('{}: {}'.format(location(), str_time))


if __name__ == '__main__':
    with Timer(4):
        print(sum(range(10 ** 7)))
    @timer(5)
    def test():
        return sum(range(10 ** 7))
    print(test())
