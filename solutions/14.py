# https://adventofcode.com/2021/day/14


import re
from collections import Counter, defaultdict

from utils.utils import get_input_path


def count_elements(input_path: str, steps: int) -> int:
    """Count elements of a polymer that is created using the rules, initial polymer and number of steps.
    Each step new elements are inserted into the polymer based on the given rules.

    :param input_path: File path of input data
    :param steps: The number of polymer insertion steps
    :return: The difference between count of most common and least common element
    """
    with open(input_path, "r") as f:
        lines = f.read().splitlines()

    # Create mapping with pair and inserted element
    rules = {}
    for line in lines[2:]:
        pair, insert = line.split(" -> ")
        rules[pair] = insert

    polymer = lines[0]
    # Create initial dict with counts for each pair
    pairs_new = {}
    for pair in rules:
        # Use a lookahead assertion to find overlapping pairs
        pairs_new[pair] = len(re.findall(f"(?=({pair}))", polymer))

    elements = defaultdict(int, dict(Counter(polymer)))
    # Keep track of elements count an pairs count while going through steps
    for step in range(steps):
        # Make copy of dict so all pairs are considered simultaneously
        pairs = pairs_new.copy()
        for pair, count in pairs_new.items():
            # Get inserted element
            insert = rules[pair]
            # Remove all original pairs, because they are now split up
            pairs[pair] -= count
            # Add as many new pairs as there were original pairs
            pairs[pair[0] + insert] += count
            pairs[insert + pair[1]] += count
            # Count the inserted elements
            elements[insert] += count

        pairs_new = pairs

    # Return difference between count of most common and least common element
    sorted_elements = sorted(elements.items(), key=lambda x: x[1], reverse=True)
    return sorted_elements[0][1] - sorted_elements[-1][1]


def main():
    # Test input
    test_file_path = get_input_path("14.txt", test=True)

    test_first_answer = count_elements(test_file_path, 10)
    assert test_first_answer == 1588
    test_second_answer = count_elements(test_file_path, 40)
    assert test_second_answer == 2188189693529

    # Real input
    file_path = get_input_path("14.txt")

    first_answer = count_elements(file_path, 10)
    assert first_answer == 2233
    second_answer = count_elements(file_path, 40)
    assert second_answer == 2884513602164


if __name__ == "__main__":
    main()
