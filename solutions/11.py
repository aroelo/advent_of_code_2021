# https://adventofcode.com/2021/day/11
import numpy as np

from utils.utils import get_input_path


def track_flashes(input_path: str, first_puzzle: bool) -> int:
    """Keeps track of octopus' energy levels in a 2D numpy array.
    For the first puzzle it counts the total number of flashes that have occurred after 100 steps.
    For the second puzzle it counts after how many steps all octopuses flash in sync.

    :param input_path: File path of input data
    :param first_puzzle: Whether the answer for the first or second puzzle is calculated
    :return: The total number of flashes after 100 steps (1st puzzle) or steps until octopuses are in sync (2nd puzzle)
    """
    levels = np.genfromtxt(input_path, delimiter=1, dtype=int)
    total_flashes = 0
    steps = 0
    while np.sum(levels) != 0:
        steps += 1
        # Increase all energy levels with 1
        levels += 1
        # Track indices of flashing and flashed octopuses
        flashing = list(zip(*np.where(levels > 9)))
        flashed = []
        while flashing:
            for row, col in flashing:
                # Increase energy level of neighboring octopuses
                row_min, row_max = max(row - 1, 0), min(row + 2, len(levels))
                col_min, col_max = max(col - 1, 0), min(col + 2, len(levels))
                levels[row_min:row_max, col_min:col_max] += 1

                # Keep track of flashed octopuses
                flashed.append((row, col))

                # Remove current flashing octopuses from list of indices
                flashing.remove((row, col))

            # Get indices of new flashing octopuses
            flashing = list(set(zip(*np.where(levels > 9))) - set(flashed))

        # Set energy levels to 0 of all octopuses that flashed
        if flashed:
            levels[tuple(zip(*flashed))] = 0
        total_flashes += len(flashed)

        if steps == 100 and first_puzzle:
            return total_flashes
    return steps


def main():
    # Test input
    test_file_path = get_input_path("11.txt", test=True)

    test_first_answer = track_flashes(test_file_path, first_puzzle=True)
    assert test_first_answer == 1656
    test_second_answer = track_flashes(test_file_path, first_puzzle=False)
    assert test_second_answer == 195

    # Real input
    file_path = get_input_path("11.txt")

    first_answer = track_flashes(file_path, first_puzzle=True)
    assert first_answer == 1652
    second_answer = track_flashes(file_path, first_puzzle=False)
    assert second_answer == 220


if __name__ == "__main__":
    main()
