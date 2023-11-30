import os


def is_path_exist(path):
    """
    Check if a given path exists.

    Parameters:
    path (str): The path to be checked.

    Returns:
    bool: True if the path exists, False otherwise.
    """
    return os.path.exists(path)
