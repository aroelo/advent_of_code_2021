# https://adventofcode.com/2021/day/12

from collections import defaultdict
from typing import Dict

from utils.utils import get_input_path


def find_paths(
    caves: Dict[str, list],
    cave: str,
    visited: set,
    path: list,
    all_paths: list,
    first_puzzle: bool,
    visit_twice: bool = True,
):
    """Recursively find all possible paths.
    For the first puzzle, small caves (lower case) can only be visited once, big caves can always be visited.
    For the second puzzle, one small cave can be visited twice, big caves can always be visited.

    :param caves: Dict with connections from 1 cave to another.
    :param cave: The current cave that is visited.
    :param visited: Set of all caves that have been visited.
    :param path: The traversed path through the cave system so far.
    :param all_paths: A list of all valid paths through the cave system.
    :param first_puzzle: Whether the answer for the first puzzle is calculated.
    :param visit_twice: If it is allowed to visit this cave twice (used for 2nd puzzle only)
    :return: A list of all possible paths.
    """
    # Add cave to path
    path.append(cave)

    # Finish path when 'end' is found and add to all_paths
    if cave == "end":
        all_paths.append(path)
        return

    # Loop through available caves from the current cave
    for next_cave in caves[cave]:
        # Big caves can always be visited and new caves can be visited
        if next_cave.isupper() or next_cave not in visited:
            # Find possible paths
            find_paths(caves, next_cave, visited | {next_cave}, path, all_paths, first_puzzle, visit_twice)
            # Set path up to the most recent cave
            path = path[: len(path) - 1 - path[::-1].index(next_cave)]
        # For the second puzzle, one small cave can be visited twice (but not the start and end cave)
        elif not first_puzzle and visit_twice and next_cave not in ["start", "end"]:
            find_paths(caves, next_cave, visited | {next_cave}, path, all_paths, first_puzzle, False)
    return all_paths


def count_paths(input_path: str, first_puzzle: bool) -> int:
    """Count the total number of possible paths through the cave system.
    Based on the input a dict is made of all connections in the cave system.
    This is used with the recursive function to find all possible paths through the cave system.

    :param input_path: File path of input data
    :param first_puzzle: Whether the answer for the first or second puzzle is calculated
    :return: Number of possible paths through the cave system.
    """
    caves = defaultdict(list)
    with open(input_path, "r") as f:
        for line in f:
            c1, c2 = line.strip("\n").split("-")
            if c1 != "end" and c2 != "start":
                caves[c1].append(c2)
            if c2 != "nd" and c1 != "start":
                caves[c2].append(c1)

    paths = find_paths(caves, "start", {"start"}, [], [], first_puzzle)

    return len(paths)


def main():
    # Test input
    test_file_path = get_input_path("12.txt", test=True)

    test_first_answer = count_paths(test_file_path, first_puzzle=True)
    assert test_first_answer == 226
    test_second_answer = count_paths(test_file_path, first_puzzle=False)
    assert test_second_answer == 3509

    # Real input
    file_path = get_input_path("12.txt")

    first_answer = count_paths(file_path, first_puzzle=True)
    assert first_answer == 4167
    second_answer = count_paths(file_path, first_puzzle=False)
    assert second_answer == 98441


if __name__ == "__main__":
    main()
