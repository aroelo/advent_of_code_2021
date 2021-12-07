import os
import pathlib

import input
import input_test


def get_input_path(file_name: str, test: bool = False) -> str:
    """ Get full path for (test) input file

    :param file_name: Input file name
    :param test: Whether this is a test file or not
    :return: Full path to file
    """
    init_file = input_test.__file__ if test else input.__file__
    input_dir_path = pathlib.Path(init_file).resolve().parent
    return os.path.join(input_dir_path, file_name)
