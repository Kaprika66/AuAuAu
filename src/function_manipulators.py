import functools
import inspect
from typing import Callable


def assert_proper_input(arg_name: str, arg_checker: Callable):
    def get_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if arg_name in kwargs:
                arg = kwargs[arg_name]
            else:
                arg_idx = __find_arg_index(func, arg_name)
                if arg_idx is None or len(args) <= arg_idx:
                    raise ValueError(f'{arg_name} argument is not provided')
                arg = args[arg_idx]
            arg_checker(arg)
            return func(*args, **kwargs)
        return wrapper
    return get_decorator


def __find_arg_index(func: Callable, arg_name: str) -> int | None:
    """Return index of function argument

    Args:
        func (Callable): Function to check
        arg_name (str): arg name to find

    Returns:
        int | None: return int if index is found, else None
    """
    arg_names = inspect.signature(func).parameters.keys()
    return next((i for i, arg in enumerate(arg_names) if arg==arg_name), None)
