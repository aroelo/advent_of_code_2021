# https://adventofcode.com/2021/day/8
from utils.utils import get_input_path


def count_easy_digits(input_path: str) -> int:
    """ Count how many times the digits 1, 4, 7 and 8 occur in the output of each display.
    These digits are easy to distinguish, as they all have a unique length of segments.

    :param input_path: File path of input data
    :return: Count of digits 1, 4, 7 and 8.
    """
    with open(input_path, "r") as f:
        displays = [line.strip("\n").split(" | ") for line in f]
    count = 0
    for display in displays:
        output = display[1].split(" ")
        for digit in output:
            if len(digit) in [2, 4, 3, 7]:
                count += 1
    return count


def calculate_sum(input_path: str) -> int:
    """ Decode the signal for each display based on first 10 signals.
    Each signal is a digit from 0-9, occurring exactly once
    After decoding get the digit for each signal in the output part of each display, the digits are joined to create a
    4 digit number.
    Finally the sum of all numbers of all displays is returned.

    :param input_path: File path of input data
    :return: Sum of output for each line
    """
    with open(input_path, "r") as f:
        displays = [line.strip("\n").split(" | ") for line in f]

    sum_out = 0
    for display in displays:
        signals, output = display[0].split(" "), display[1].split(" ")

        sorted_signals = sorted([set(s) for s in signals], key=len)
        digits = {1: sorted_signals[0],
                  4: sorted_signals[2],
                  7: sorted_signals[1],
                  8: sorted_signals[9]}
        # Digits 0, 6, 9 all have length 6
        for signal in sorted_signals[6:9]:
            if digits[4] <= signal:
                digits[9] = signal
            else:
                if digits[7] <= signal:
                    digits[0] = signal
                else:
                    digits[6] = signal
        # Digits 2, 3, 5 all have length 5
        for signal in sorted_signals[3:6]:
            if digits[1] <= signal:
                digits[3] = signal
            else:
                if signal <= digits[6]:
                    digits[5] = signal
                else:
                    digits[2] = signal

        # Recreate digits dict, swapping key and values
        digits = {"".join(sorted(v)): k for k, v in digits.items()}
        # Look up digit based on given signal and create 4 digit number
        out = ""
        for signal in output:
            out += str(digits["".join(sorted(signal))])
        sum_out += int(out)
    return sum_out


def main():
    # Test input
    test_file_path = get_input_path("8.txt", test=True)

    test_first_answer = count_easy_digits(test_file_path)
    assert test_first_answer == 26
    test_second_answer = calculate_sum(test_file_path)
    assert test_second_answer == 61229

    # Real input
    file_path = get_input_path("8.txt")

    first_answer = count_easy_digits(file_path)
    assert first_answer == 352
    second_answer = calculate_sum(file_path)
    assert second_answer == 936117


if __name__ == "__main__":
    main()
