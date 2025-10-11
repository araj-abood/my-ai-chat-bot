import os
def get_abs_path(path):
    return os.path.abspath(path)


def is_with_in_directory(directory_path, target_path):

    return target_path.startswith(directory_path)