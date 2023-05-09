import time
import functools
# from typing import Tuple


def timer(fonction):
    """Sert à chronométrer une action donnée"""
    @functools.wraps(fonction)
    def wrap(*param, **param2):
        start = time.perf_counter()
        try:
            value = fonction(*param, **param2)
        except Exception as ex:
            print(str(ex))
            value = None
        end = time.perf_counter()
        runTime = end - start
        return value, runTime
    return wrap



def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug
