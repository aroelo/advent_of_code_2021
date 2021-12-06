# https://adventofcode.com/2021/day/6
from utils.utils import get_input_path
from collections import OrderedDict, Counter


def count_lanternfish(input_path: str, days: int) -> int:
    """ Count the number of lanternfish after x number of days

    :param input_path: File path of input data
    :param days: Number of days
    :return: How many lanternfish there are after given number of days
    """
    with open(input_path, "r") as f:
        initial_fish = list(map(int, f.read().split(",")))

    # Create initial dict with fish grouped by age
    grouped_fish = OrderedDict({age: 0 for age in range(10)})
    grouped_fish.update(Counter(initial_fish))

    for day in range(1, days + 1):
        # Create new fishes with age 9, so fish with age 8 will be set to this number below
        grouped_fish[9] = grouped_fish[0]
        # Add fishes with age 7, they will be added to fish with age 6 below
        grouped_fish[7] += grouped_fish[0]
        for age in range(9):
            grouped_fish[age] = grouped_fish[age+1]
        print(f"After {day} {'day' if day==1 else 'days'}: {grouped_fish}")
    return sum(grouped_fish[age] for age in range(9))


def main():
    # Test input
    test_file_path = get_input_path("6.txt", test=True)

    test_first_answer = count_lanternfish(test_file_path, days=80)
    assert test_first_answer == 5934
    test_second_answer = count_lanternfish(test_file_path, days=256)
    assert test_second_answer == 26984457539

    # Real input
    file_path = get_input_path("6.txt")

    first_answer = count_lanternfish(file_path, days=80)
    assert first_answer == 389726
    second_answer = count_lanternfish(file_path, days=256)
    assert second_answer == 1743335992042


if __name__ == "__main__":
    main()
