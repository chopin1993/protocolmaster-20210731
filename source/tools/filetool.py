import os


def get_file_list(root, key=None):
    files = os.listdir(root)
    if key is not None:
        files.sort(key=key)
    return files