# https://adventofcode.com/2021/day/9
import numpy as np
from scipy.ndimage import label

from utils.utils import get_input_path


def sum_risk_levels(input_path: str) -> int:
    """ Find the low points in a heightmap and calculate the total risk level.
    The risk level of a low point is 1 plus its height.

    :param input_path: File path of input data
    :return: Sum of the risk levels of all low points.
    """
    heightmap = np.genfromtxt(input_path, delimiter=1, dtype=int)
    rows, columns = heightmap.shape

    left = np.diff(heightmap, axis=1)
    left = np.append(left, np.full((rows, 1), 1), axis=1)

    right = np.diff(np.fliplr(heightmap), axis=1)
    right = np.insert(np.fliplr(right), 0, [1], axis=1)

    down = np.diff(np.flipud(heightmap), axis=0)
    down = np.insert(np.flipud(down), 0, np.full((1, columns), 1), axis=0)

    up = np.diff(heightmap, axis=0)
    up = np.append(up, np.full((1, columns), 1), axis=0)

    low_points = heightmap[np.logical_and(down > 0, up > 0) & np.logical_and(left > 0, right > 0)]
    return sum(low_points) + len(low_points)


def find_basins(input_path: str) -> int:
    """ Find the three largest basins and multiply their sizes.
    A basin consists of connected segments, they are bordered by 9's.

    :param input_path: File path of input data
    :return: Multiplied size of 3 largest basins
    """
    heightmap = np.genfromtxt(input_path, delimiter=1, dtype=int)
    # Restructure array, set 9's to 0's and all other values to 1
    binary_heightmap = np.abs(np.clip(heightmap, 8, 9) - 9)
    # Create labels, each segment is labeled with a different number
    labels, no_labels = label(binary_heightmap)
    # Count size of three largest basins (largest label is ignored, these are the original 9's)
    return np.prod((sorted(np.bincount(np.reshape(labels, labels.size)))[-4:-1]))


def main():
    # Test input
    test_file_path = get_input_path("9.txt", test=True)

    test_first_answer = sum_risk_levels(test_file_path)
    assert test_first_answer == 15
    test_second_answer = find_basins(test_file_path)
    assert test_second_answer == 1134

    # Real input
    file_path = get_input_path("9.txt")

    first_answer = sum_risk_levels(file_path)
    assert first_answer == 633
    second_answer = find_basins(file_path)
    assert second_answer == 1050192


if __name__ == "__main__":
    main()
