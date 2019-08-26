import os
import importlib


def import_all_python(path):
    for file in os.listdir(path):
        if file.endswith(".py"):
            module_name = os.path.splitext(os.path.split(file)[1])[0]
            importlib.import_module(module_name)


