import functools
import inspect
import re
from typing import Callable, Iterable


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


class FuncFactory:
    def __init__(self, module, regex: str) -> None:
        self._functions = self._load_extractors(module, regex)

    def execute_func(self, func_name: str, *args, **kwargs) -> any:
        return self.functions[func_name](*args, **kwargs)

    def _load_extractors(self, base_module, regex: str):
        functions = self._module_functions(base_module)
        filtered_functions = self._filter_functions(functions, regex)
        return dict(filtered_functions)

    def _module_functions(self, module):
        submodules = self._submodules_iter(module)
        all_functions = []
        for _, module in [("base_module", module)] + submodules:
            all_functions.extend(inspect.getmembers(
            module, inspect.isfunction
            ))
        return all_functions

    def _submodules_iter(self, module):
        return inspect.getmembers(
            module, inspect.ismodule
        )

    def _filter_functions(self, functions: list[str, Callable], regex: str) -> Iterable[tuple[str, Callable]]:
        return filter(
            lambda t: bool(re.search(regex, t[0])),
            functions
        )

    @property
    def functions(self) -> dict[str, Callable]:
        """
        Returns:
            dict[str, Callable]: dict with functions as values and theirs names as keys.
        """
        return self._functions



def main():
    import importlib
    import sys
    sys.path.append(".")
    features = importlib.import_module("features")

    factory = FuncFactory(features, r"^add_\w*_feature$")
    for extractor in factory.functions.items():
        print(extractor)


if __name__ == "__main__":
    main()
