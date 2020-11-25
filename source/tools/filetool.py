import os


def get_file_list(root, key=None):
    files = os.listdir(root)
    if key is not None:
        files.sort(key=key)
    return files


def get_config_file(name):
    return os.path.join(os.path.dirname(__file__), ".." , "resource", name)