# https://adventofcode.com/2021/day/5
from utils.utils import get_input_path
import numpy as np
import re


def find_hydrothermal_vents(file_path: str, first_puzzle: bool) -> int:
    """ Count the number of overlapping points of hydrothermal vents.
    A matrix is used to store the number of times a hydrothermal vent is found in that position.
    All positions which are covered more than once are counter, for the first puzzle diagonal vents do not count.

    :param file_path: File path of input data
    :param first_puzzle: Whether the answer for the first or second puzzle is calculated
    :return: The number of points where are least two lines overlap
    """
    matrix = np.zeros(shape=(1000, 1000), dtype=int)
    with open(file_path, "r") as f:
        for line in f:
            coordinates = re.split(" -> |,", line.strip("\n"))
            x1, y1, x2, y2 = map(int, coordinates)

            # vertical
            if x1 == x2:
                y = sorted([y1, y2])
                matrix[y[0]: y[1]+1, x1] += 1
            # horizontal
            elif y1 == y2:
                x = sorted([x1, x2])
                matrix[y1, x[0]: x[1]+1] += 1
            # diagonal
            else:
                if first_puzzle:
                    continue
                # Sort based on x values, point a is to the left of point b
                point_a, point_b = sorted([(x1, y1), (x2, y2)], key=lambda i: i[0])
                x1, y1, x2, y2 = point_a[0], point_a[1], point_b[0], point_b[1]
                # Diagonal is going up
                if y1 > y2:
                    matrix_subset = matrix[y2:y1+1, x1:x2+1]
                    np.fill_diagonal(np.flipud(matrix_subset),
                                     np.flipud(matrix_subset).diagonal() + 1)
                # Diagonal is going down
                else:
                    matrix_subset = matrix[y1:y2+1, x1:x2+1]
                    np.fill_diagonal(matrix_subset, matrix_subset.diagonal() + 1)

    return len(matrix[matrix > 1])


def main():
    # Test input
    test_file_path = get_input_path("5.txt", test=True)

    test_first_answer = find_hydrothermal_vents(test_file_path, first_puzzle=True)
    assert test_first_answer == 5
    test_second_answer = find_hydrothermal_vents(test_file_path, first_puzzle=False)
    assert test_second_answer == 12

    # Real input
    file_path = get_input_path("5.txt")

    first_answer = find_hydrothermal_vents(file_path, first_puzzle=True)
    assert first_answer == 6841
    second_answer = find_hydrothermal_vents(file_path, first_puzzle=False)
    assert second_answer == 19258


if __name__ == "__main__":
    main()
