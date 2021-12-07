# https://adventofcode.com/2021/day/7
from utils.utils import get_input_path
import statistics


def calculate_fuel_cost_median(input_path: str) -> int:
    """ Calculate total fuel costs for all crabs to move horizontally to optimal position, 1 move == 1 fuel

    :param input_path: File path of input data
    :return: Total fuel cost
    """
    with open(input_path, "r") as f:
        positions = list(map(int, f.read().split(",")))
    optimal_position = statistics.median(positions)
    return sum([abs(pos - optimal_position) for pos in positions])


def calculate_fuel_cost_triangular(input_path: str) -> int:
    """ Calculate total fuel costs for all crabs to move horizontally to optimal position, costs of moving to the
    optimal position are calculated using the nth triangular number.

    :param input_path: File path of input data
    :return: Total fuel cost
    """
    with open(input_path, "r") as f:
        positions = list(map(int, f.read().split(",")))

    lowest_cost = None
    for x in range(max(positions)):
        fuel_cost = sum([(abs(pos - x) * (abs(pos - x) + 1) // 2) for pos in positions])
        if not lowest_cost or fuel_cost < lowest_cost:
            lowest_cost = fuel_cost
    return lowest_cost


def main():
    # Test input
    test_file_path = get_input_path("7.txt", test=True)

    test_first_answer = calculate_fuel_cost_median(test_file_path)
    assert test_first_answer == 37
    test_second_answer = calculate_fuel_cost_triangular(test_file_path)
    assert test_second_answer == 168

    # Real input
    file_path = get_input_path("7.txt")

    first_answer = calculate_fuel_cost_median(file_path)
    assert first_answer == 357353
    second_answer = calculate_fuel_cost_triangular(file_path)
    assert second_answer == 104822130


if __name__ == "__main__":
    main()
