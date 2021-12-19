# https://adventofcode.com/2021/day/17
import re

from utils.utils import get_input_path


def find_velocity_values(input_path: str, first_puzzle: bool) -> int:
    """Given the target area from the input file, find all possible initial velocity positions (x and y) that will
    land the projectile in the target area.

    :param input_path: File path of input data
    :param first_puzzle: Whether the answer for the first puzzle is calculated.
    :return: The highest possible peak (1st puzzle) or amount of valid initial velocity positions.
    """

    with open(input_path, "r") as f:
        _, x_min, x_max, _, y_min, y_max = re.split(",|\.\.|=", f.read())
    x_min, x_max, y_min, y_max = int(x_min), int(x_max), int(y_min), int(y_max)

    positions = set()
    overshoot = False
    y_max_peak = 0
    # Increase values of y, starting at y_min, until the projectile overshoots
    y = y_min
    while not overshoot:
        overshoot = True
        y_abyss = None
        if y <= 0:
            # Decrease starts right away
            y_steps = 0
            # Peak is always zero
            y_peak = 0
        else:
            # Decrease starts after y steps
            y_steps = y
            # Peak is triangular number of y, e.g. if y=4: 4+3+2+1
            y_peak = y * (y + 1) / 2
        # Keep increasing steps of y until the abyss has gone below y_min
        while y_abyss is None or y_abyss >= y_min:
            # Calculate the y abyss
            if y <= 0:
                # The abyss is the sum of all steps e.g. if y=4: 4+3+2+1
                y_abyss = sum([y - i for i in range(0, y_steps)])
            else:
                # The abyss is the peak minus the triangular number of y_steps
                y_abyss = y_peak - (y_steps * (y_steps + 1) / 2)

            # If y_abyss is not 0 and not below y_min, it did not overshoot yet
            if y_min <= y_abyss < 0:
                overshoot = False

            # If y_abyss is in the target area
            if y_min <= y_abyss <= y_max:
                # Store the peak as max peak
                y_max_peak = y_peak
                # Get all valid x positions for this y position
                for x in range(1, x_max + 1):
                    # Given the initial x value, calculate the x position after y_steps
                    if y <= 0:
                        x_forward = sum([x - i for i in range(0, y_steps)])
                    else:
                        x_forward = sum([max(0, x - i) for i in range(0, y_steps + y + 1)])
                    # If x value (and y value) are in target area, add to possible positions
                    if x_min <= x_forward <= x_max:
                        positions.add((x, y))
                    elif x_forward >= x_max:
                        break
            y_steps += 1
        y += 1

    return int(y_max_peak) if first_puzzle else len(positions)


def main():
    # Test input
    test_file_path = get_input_path("17.txt", test=True)

    test_first_answer = find_velocity_values(test_file_path, True)
    assert test_first_answer == 45
    test_second_answer = find_velocity_values(test_file_path, False)
    assert test_second_answer == 112
    #
    # Real input
    file_path = get_input_path("17.txt")

    first_answer = find_velocity_values(file_path, True)
    assert first_answer == 15400
    second_answer = find_velocity_values(file_path, False)
    assert second_answer == 5844


if __name__ == "__main__":
    main()
