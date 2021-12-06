# https://adventofcode.com/2021/day/3
from utils.utils import get_input_path
import numpy as np
import operator
from typing import Callable


def power_consumption(file_path: str) -> int:
    """ Calculate the power consumption

    :param file_path: File path of input data
    :return: The calculated power consumption
    """
    data = np.genfromtxt(file_path, delimiter=1, dtype=int)
    gamma_binary = 0b00
    no_bits = data.shape[1]
    data_size = data.shape[0]
    for i, col in enumerate(data.sum(axis=0)):
        binary = f"0b{'0'*i}{int(col>(data_size/2))}{'0'*(no_bits-1-i)}"
        gamma_binary += eval(binary)
    epsilon_binary = ~gamma_binary & eval(f"0b{'1'*no_bits}")

    return gamma_binary * epsilon_binary


def filter_data(file_path: str, operator_func: Callable) -> int:
    """ Loops through columns of data array and filters row based on whether there are mostly 1's or 0's in that row

    :param file_path: Path to file input
    :param operator_func: Operator function, used to confirm whether two parts are equal or not equal
    :return: Remaining binary
    """
    data = np.genfromtxt(file_path, delimiter=1, dtype=int)
    for i in range(np.shape(data)[1]):
        data = data[np.where(operator_func(data[:, i], int(data.sum(axis=0)[i] >= len(data) / 2)))]
        if len(data) == 1:
            break
    return int(str(data[0]).strip("[]").replace(" ", ""), 2)


def life_support_rating(file_path: str) -> int:
    """ Get the life support rating by calculating both oxygen generator and co2 scrubber rating

    :param file_path: File path of input data
    :return: The life support rating
    """
    oxygen_generator_rating = filter_data(file_path, operator.eq)

    co2_scrubber_rating = filter_data(file_path, operator.ne)

    return oxygen_generator_rating * co2_scrubber_rating


def main():
    # Test input
    test_file_path = get_input_path("3.txt", test=True)

    test_first_answer = power_consumption(test_file_path)
    assert test_first_answer == 198
    test_second_answer = life_support_rating(test_file_path)
    assert test_second_answer == 230

    # Real input
    file_path = get_input_path("3.txt")

    first_answer = power_consumption(file_path)
    assert first_answer == 3885894
    second_answer = life_support_rating(file_path)
    assert second_answer == 4375225


if __name__ == "__main__":
    main()
