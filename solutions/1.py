# https://adventofcode.com/2021/day/1
from utils.utils import get_input_path


def no_depth_increase(file_path: str) -> int:
    """ Count number of times a depth measurement increases

    :param file_path: File path of input data
    :return: The number of times the depth increased
    """
    increased = 0
    prev_depth = None
    with open(file_path, "r") as f:
        for line in f:
            depth = int(line.strip("\n"))
            if prev_depth and depth > prev_depth:
                increased += 1
            prev_depth = depth
    return increased


def no_depth_increase_window(file_path: str) -> int:
    """ Count number of times a depth measurement increases based on a three-measurement sliding window

    :param file_path: File path of input data
    :return: The number of times the depth increased
    """
    with open(file_path, "r") as f:
        depths = [int(line.strip("\n")) for line in f]

    window_size = 3
    windows = [depths[i:i + window_size] for i in range(len(depths) - window_size + 1)]

    increased = 0
    prev_window = None
    for window in windows:
        if prev_window and sum(window) > prev_window:
            increased += 1
        prev_window = sum(window)
    return increased


def main():
    # Test input
    test_file_path = get_input_path("1.txt", test=True)

    test_first_answer = no_depth_increase(test_file_path)
    assert test_first_answer == 7
    test_second_answer = no_depth_increase_window(test_file_path)
    assert test_second_answer == 5

    # Real input
    file_path = get_input_path("1.txt")

    first_answer = no_depth_increase(file_path)
    assert first_answer == 1532
    second_answer = no_depth_increase_window(file_path)
    assert second_answer == 1571


if __name__ == "__main__":
    main()
