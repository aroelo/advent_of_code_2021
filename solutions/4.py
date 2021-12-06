# https://adventofcode.com/2021/day/4
from utils.utils import get_input_path
from typing import List
from collections import defaultdict
from textwrap import wrap


def get_boards_info(lines: list) -> List[dict]:
    """ From input lines create a list of boards.
    Each board is a dict storing count information (for each row and column) and a mapping of the row and column for
    each number in the board.

    :param lines: Lines with board numbers
    :return: List with boards info
    """
    boards = []
    board = {"counts": [defaultdict(int), defaultdict(int)], "map": {}}
    for row, line in enumerate(lines[2:]):
        row = row % 6
        if row == 5:
            boards.append(board)
            board = {"counts": [defaultdict(int), defaultdict(int)], "map": {}}
        board["map"].update({number: (row, col) for col, number in enumerate(wrap(line, 2))})

    boards.append(board)
    return boards


def get_bingo_scores(file_path: str, first_puzzle: bool) -> [int, int]:
    """ Given the numbers that are drawn and boards info, find the first and last board to get bingo.
    Bingo is found by using the map to look up the row and column for each number, when a row or column has a count
    of 5 that board has bingo.
    Numbers that are drawn are removed from each board.
    Boards are removed from the list if they obtain bingo.

    :param file_path: File path of input data
    :param first_puzzle: Whether the answer for the first or second puzzle is calculated
    :return: Sum of remaining numbers of the winner (1st puzzle) or loser (2nd puzzle) board.
    """
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f]

    numbers = lines[0].split(",")
    boards = get_boards_info(lines)

    winner_score = 0
    last_board = None
    last_number = None
    for number in numbers:
        number = number.strip(" ")
        for board in boards[:]:
            # Get row and column while removing number from map
            row, col = board["map"].pop(number, (None, None))
            if row is None:
                continue

            for i, row_or_col in enumerate([row, col]):
                # Increase count for the given row and column
                board["counts"][i][row_or_col] += 1

                # Check for bingo
                if board["counts"][i][row_or_col] == 5:
                    boards.remove(board)
                    if winner_score == 0:
                        # Calculate score for the first board to get bingo
                        sum_numbers = sum([int(key) for key in board["map"]])
                        winner_score = sum_numbers * int(number)

                    if first_puzzle:
                        return winner_score

                    # Store info for potential last board to get bingo
                    last_board = board
                    last_number = number
                    break

    loser_score = sum([int(key) for key in last_board["map"]]) * int(last_number)
    return loser_score


def main():
    # Test input
    test_file_path = get_input_path("4.txt", test=True)

    test_first_answer = get_bingo_scores(test_file_path, first_puzzle=True)
    assert test_first_answer == 4512
    test_second_answer = get_bingo_scores(test_file_path, first_puzzle=False)
    assert test_second_answer == 1924

    # Real input
    file_path = get_input_path("4.txt")

    first_answer = get_bingo_scores(file_path, first_puzzle=True)
    assert first_answer == 87456
    second_answer = get_bingo_scores(file_path, first_puzzle=False)
    assert second_answer == 15561


if __name__ == "__main__":
    main()
