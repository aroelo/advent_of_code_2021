# https://adventofcode.com/2021/day/10
import re
from statistics import median_low

from utils.utils import get_input_path


def syntax_error_score(input_path: str, first_puzzle: bool) -> int:
    """ For the first puzzle, calculate the error score by finding the first incorrect closing character on corrupted
    lines.
    For the second puzzle calculate the autocomplete score for incomplete lines, corrupt lines are ignored.

    :param input_path: File path of input data
    :param first_puzzle: Whether the answer for the first or second puzzle is calculated
    :return: The error score (1st puzzle) or middle autocomplete score (2nd puzzle)
    """
    with open(input_path, "r") as f:
        lines = f.read().splitlines()

    # Create maps with error and autocomplete scores
    error_map = {")": 3, "]": 57, "}": 1197, ">": 25137}
    autocomplete_map = {"(": 1, "[": 2, "{": 3, "<": 4}

    error_score = 0
    autocomplete_scores = []
    for line in lines:
        # Strip pairs of opening and closing chars, until none are left
        no_sub = True
        while no_sub > 0:
            line, no_sub = re.subn("<>|\[\]|\{\}|\(\)", "", line)

        # Find the first closing character, this is the incorrect one
        match = re.search(">|\}|\)|\]", line)

        # Calculate the error score for first puzzle
        if match:
            error_score += error_map[match.group(0)]
        # Calculate the autocomplete score for second puzzle
        else:
            line_score = 0
            for char in line[::-1]:
                line_score = (line_score * 5) + autocomplete_map[char]
            autocomplete_scores.append(line_score)

    score = error_score if first_puzzle else median_low(autocomplete_scores)
    return score


def main():
    # Test input
    test_file_path = get_input_path("10.txt", test=True)

    test_first_answer = syntax_error_score(test_file_path, first_puzzle=True)
    assert test_first_answer == 26397
    test_second_answer = syntax_error_score(test_file_path, first_puzzle=False)
    assert test_second_answer == 288957

    # Real input
    file_path = get_input_path("10.txt")

    first_answer = syntax_error_score(file_path, first_puzzle=True)
    assert first_answer == 296535
    second_answer = syntax_error_score(file_path, first_puzzle=False)
    assert second_answer == 4245130838


if __name__ == "__main__":
    main()
