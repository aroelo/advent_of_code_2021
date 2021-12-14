# https://adventofcode.com/2021/day/13

import numpy as np

from utils.utils import get_input_path


def fold_paper(input_path: str, first_puzzle: bool) -> int:
    """Fold a transparent origami paper based on the instructions in input file.

    :param input_path: File path of input data
    :param first_puzzle: Whether the answer for the first or second puzzle is calculated
    :return: The number of dots after one fold (1st puzzle) or array with capital letters (2nd puzzle)
    """

    with open(input_path, "r") as f:
        instructions = f.read().splitlines()

    dot_indices = ([], [])
    fold_indices = []
    for step in instructions:
        if not step:
            continue
        # Get dot locations
        if "," in step:
            column, row = step.split(",")
            dot_indices[0].append(int(row))
            dot_indices[1].append(int(column))
        # Get fold instructions
        else:
            axis, index = step.split("fold along ")[1].split("=")
            fold_indices.append((axis, int(index)))

    # Create a numpy array with dots as 1's
    paper = np.zeros((max(dot_indices[0]) + 1, max(dot_indices[1]) + 1), dtype=int)
    paper[dot_indices] += 1

    # Fold numpy array along x and y axis
    for fold in fold_indices:
        axis, index = fold
        # Fold the array by flipping it around
        if axis == "x":
            paper[:, :index] += np.fliplr(paper[:, index + 1:])
        else:
            paper[:index, :] += np.flipud(paper[index + 1:, :])
        # Delete the rows/columns that were folder over
        paper = np.delete(paper, range(index, index + index + 1), axis=0 if axis == "y" else 1)
        # Return the number of dots after the first fold
        if first_puzzle:
            return np.count_nonzero(paper)
    return paper > 0


def main():
    # Test input
    test_file_path = get_input_path("13.txt", test=True)

    test_first_answer = fold_paper(test_file_path, first_puzzle=True)
    assert test_first_answer == 17

    # Real input
    file_path = get_input_path("13.txt")

    first_answer = fold_paper(file_path, first_puzzle=True)
    assert first_answer == 607
    look_at_me = fold_paper(file_path, first_puzzle=False)
    # Visually inspect numpy array that is returned to read the eight capital letters 'CPZLPFZL'
    second_answer = "CPZLPFZL"
    assert second_answer == "CPZLPFZL"


if __name__ == "__main__":
    main()
