# https://adventofcode.com/2021/day/16


from utils.utils import get_input_path


def parse_packet(binary_str: str) -> [int, int, int]:
    """Given the binary_str, recursively go through all the (sub)packets represented by the binary str.
    Packets with a type id of '100' are literal values, while other packets are operator packets that contain a given
    number of sub-packets.

    :param binary_str: Binary representation of the original hexadecimal transmission.
    :return: The summed versions, value of the packets and no of bits in the packet
    """
    version = int(binary_str[0:3], 2)
    type_id = binary_str[3:6]
    # Packet represents literal value
    if type_id == "100":
        last_group = False
        i = 0
        value = ""
        while not last_group:
            last_group = binary_str[6 + i] == "0"
            value += binary_str[7 + i: 11 + i]
            i += 5
        bits = 6 + i
        return version, int(value, 2), bits
    # Packet is an operator with sub-packets
    else:
        total_value = None
        version_sum = version
        bits_subpackets = 0
        no_subpackets = 0

        # Get the length type and how many sub-packets there are (given in bits or no. packets)
        len_type_id = binary_str[6]
        len_type_id_bits = 15 if len_type_id == "0" else 11
        total_bits_no_subpackets = int(binary_str[7: 7 + len_type_id_bits], 2)

        # Get all sub-packets
        bits_no_subpackets = 0
        while bits_no_subpackets < total_bits_no_subpackets:
            version, value, bits = parse_packet(binary_str[7 + len_type_id_bits + bits_subpackets:])

            bits_subpackets += bits
            no_subpackets += 1
            bits_no_subpackets = bits_subpackets if len_type_id == "0" else no_subpackets

            version_sum += version

            if total_value is None:
                total_value = value
            else:
                if type_id == "000":
                    total_value += value
                elif type_id == "001":
                    total_value *= value
                elif type_id == "010":
                    total_value = min(total_value, value)
                elif type_id == "011":
                    total_value = max(total_value, value)
                elif type_id == "101":
                    total_value = int(total_value > value)
                elif type_id == "110":
                    total_value = int(total_value < value)
                elif type_id == "111":
                    total_value = int(total_value == value)

        bits = bits_subpackets + len_type_id_bits + 7
        return version_sum, total_value, bits


def read_hexadecimal_input(input_path: str) -> str:
    """Read the hexadecimal transmission from the input file.

    :param input_path: File path of input data
    :return: Hexadecimal string
    """
    with open(input_path, "r") as f:
        hexadecimals = f.read().strip("\n")

    return hexadecimals


def decode_hexadecimal_transmission(hexadecimals: str, first_puzzle: bool) -> int:
    """Decode the given hexadecimal transmission.

    :param hexadecimals: Hexadecimal string with transmission bits
    :param first_puzzle: Whether the answer for the first puzzle is calculated.
    :return: The sum of all (sub)packet versions (1st puzzle) or value of outermost packet (2nd puzzle)
    """

    binary_str = bin(int(hexadecimals, 16))[2:]
    starting_zeros = len(hexadecimals) - len(hexadecimals.lstrip("0"))
    binary_str = "0000" * starting_zeros + binary_str
    if len(binary_str) % 4 != 0:
        binary_str = "0" * (4 - len(binary_str) % 4) + binary_str

    version, value, _ = parse_packet(binary_str)

    return version if first_puzzle else value


def main():
    # Test input
    assert decode_hexadecimal_transmission("8A004A801A8002F478", True) == 16
    assert decode_hexadecimal_transmission("620080001611562C8802118E34", True) == 12
    assert decode_hexadecimal_transmission("C0015000016115A2E0802F182340", True) == 23
    assert decode_hexadecimal_transmission("A0016C880162017C3686B18A3D4780", True) == 31

    assert decode_hexadecimal_transmission("C200B40A82", False) == 3  # Sum of 1 and 2
    assert decode_hexadecimal_transmission("04005AC33890", False) == 54  # Product of 6 and 9
    assert decode_hexadecimal_transmission("880086C3E88112", False) == 7  # Minimum of 7, 8, 9
    assert decode_hexadecimal_transmission("CE00C43D881120", False) == 9  # Maximum of 7, 8, 9
    assert decode_hexadecimal_transmission("D8005AC2A8F0", False) == 1  # If 5 < 15
    assert decode_hexadecimal_transmission("F600BC2D8F", False) == 0  # If 5 > 15
    assert decode_hexadecimal_transmission("9C005AC2F8F0", False) == 0  # If 5 == 15
    assert decode_hexadecimal_transmission("9C0141080250320F1802104A08", False) == 1

    # Real input
    file_path = get_input_path("16.txt")
    hexadecimals = read_hexadecimal_input(file_path)

    first_answer = decode_hexadecimal_transmission(hexadecimals, True)
    assert first_answer == 927
    second_answer = decode_hexadecimal_transmission(hexadecimals, False)
    assert second_answer == 1725277876501


if __name__ == "__main__":
    main()
