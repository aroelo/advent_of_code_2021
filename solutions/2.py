# https://adventofcode.com/2021/day/2
from utils.utils import get_input_path


def calculate_position(file_path: str) -> int:
    """ Calculate final position.
    Forward increases horizontal position, down increases depth, up decreases depth

    :param file_path: File path of input data
    :return: Horizontal position multiplied by depth
    """
    location = {"forward": 0, "down": 0, "up": 0}
    with open(file_path, "r") as f:
        for line in f:
            move, value = line.strip().split(" ")
            location[move] += int(value)
    horizontal, depth = (location["forward"], location["down"]-location["up"])
    return horizontal * depth


def calculate_position2(file_path: str) -> int:
    """ Calculate final position.
    Forward increases horizontal position with X and depth by aim times X
    Down increases aim with X
    Up decreases aim with X

    :param file_path: File path of input data
    :return: Horizontal position multiplied by depth
    """
    horizontal = 0
    depth = 0
    aim = 0
    with open(file_path, "r") as f:
        for line in f:
            move, unit = line.strip().split(" ")
            if move == "forward":
                horizontal += int(unit)
                depth += (aim * int(unit))
            elif move == "down":
                aim += int(unit)
            else:
                aim -= int(unit)
    return horizontal * depth


def main():
    # Test input
    test_file_path = get_input_path("2.txt", test=True)

    test_first_answer = calculate_position(test_file_path)
    assert test_first_answer == 150
    test_second_answer = calculate_position2(test_file_path)
    assert test_second_answer == 900

    # Real input
    file_path = get_input_path("2.txt")

    first_answer = calculate_position(file_path)
    assert first_answer == 2187380
    second_answer = calculate_position2(file_path)
    assert second_answer == 2086357770


if __name__ == "__main__":
    main()
