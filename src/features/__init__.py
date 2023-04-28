import importlib
import os

current_dir = os.path.dirname(__file__)
module_files = [f for f in os.listdir(current_dir) if f.endswith(".py") and f != "__init__.py"]

for module_file in module_files:
    module_name = os.path.splitext(module_file)[0]
    # print("from init", module_name)
    ret = importlib.import_module("." + module_name, __package__)
    # print(ret)
