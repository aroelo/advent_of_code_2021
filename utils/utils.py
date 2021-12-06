import os
import pathlib

import input
import input_test


def get_input_path(file_path: str, test: bool = False) -> str:
    """

    :param file_path:
    :param test:
    :return:
    """
    init_file = input_test.__file__ if test else input.__file__
    input_dir_path = pathlib.Path(init_file).resolve().parent
    return os.path.join(input_dir_path, file_path)
