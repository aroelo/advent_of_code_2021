# https://adventofcode.com/2021/day/15

import heapq
import sys
from collections import defaultdict
from typing import Dict, List, Tuple

import numpy as np

from utils.utils import get_input_path


def create_risks_matrix(input_path: str, first_puzzle: bool) -> np.array:
    """Create a 2D numpy array representing risk levels based on the input data.
    For the first puzzle, the input data represents the matrix.
    For the second puzzle, the input data is just the top left tile of a 5x5 tiled matrix. The top left tile is
    repeated to the right and downward, but all risk levels are 1 level higher. The maximum risk level is 9,
    anything above that will wrap back around to 1.

    :param input_path: File path of input data
    :param first_puzzle: Whether the answer for the first puzzle is calculated.
    :return: Matrix with risk levels
    """
    risks = np.genfromtxt(input_path, delimiter=1, dtype=int)
    if first_puzzle:
        return risks
    else:
        size = int(risks.size ** 0.5)
        tiled_risks = np.zeros((size * 5, size * 5), dtype=int)
        for row_increase, i in enumerate(range(0, size * 5, size)):
            for col_increase, j in enumerate(range(0, size * 5, size)):
                tiled_risks[i : i + size, j : j + size] = (risks + row_increase + col_increase) % 9
        tiled_risks[tiled_risks == 0] = 9
        return tiled_risks


def create_node_graph(risks: np.array, size: int) -> Dict[Tuple[int, int], List[Tuple[Tuple[int, int], int]]]:
    """Create a graph with each node in the risks array as keys.
    For each node all neighboring nodes and the distance to those are included as values.

    :param risks: 2D numpy array with risk levels for each node
    :param size: Number of rows and columns of the array
    :return: The graph with node information.
    """
    graph = {}
    for i in range(size):
        for j in range(size):
            left = ((i, j - 1), risks[i][j - 1]) if j > 1 else None
            right = ((i, j + 1), risks[i][j + 1]) if j < size - 1 else None
            up = ((i - 1, j), risks[i - 1][j]) if i > 1 else None
            down = ((i + 1, j), risks[i + 1][j]) if i < size - 1 else None
            graph[(i, j)] = list(filter(None, [left, right, up, down]))
    return graph


def calculate_lowest_risk(input_path: str, first_puzzle: bool) -> int:
    """Given the square cavern described by input data, find the optimal path from the top left position to the
    bottom right position. The optimal path has the lowest total risk and is found using Dijkstra's algorithm.
    Finally, return the total risk level of the optimal path.

    :param input_path: File path of input data
    :param first_puzzle: Whether the answer for the first puzzle is calculated.
    :return: The total risk level of the optimal path.
    """
    # Create matrix with risk values for each node
    risks = create_risks_matrix(input_path, first_puzzle)
    size = int(risks.size ** 0.5)

    # Create graph with neighbors + dist to each node
    graph = create_node_graph(risks, size)

    # Dictionary with all nodes and shortest distance to node 0,0
    dist_to_start = defaultdict(lambda: sys.maxsize)
    dist_to_start[(0, 0)] = 0

    # Create queue which includes neighboring nodes sorted by distance to node 0,0
    queue = []
    heapq.heappush(queue, (0, (0, 0)))

    # Set to keep track of which nodes have been finalised
    visited = set()

    while queue:
        # Get current node and distance
        dist, node = heapq.heappop(queue)
        if node in visited:
            continue

        # Go through all neighbors of node and update distance values
        neighbors = graph[node]
        for neighbor in neighbors:
            neighbor_node, neighbor_dist = neighbor
            new_dist = neighbor_dist + dist
            old_dist = dist_to_start[neighbor_node]

            # If new distance is shorter, update distance in dict and add node to queue
            if new_dist < old_dist:
                dist_to_start[neighbor_node] = new_dist
                # Adds item to queue and maintains sorted queue
                heapq.heappush(queue, (new_dist, neighbor_node))

    return dist_to_start[(size - 1, size - 1)]


def main():
    # Test custom test input that includes a loop in optimal path
    test_file_path = get_input_path("15_loop.txt", test=True)

    test_first_answer = calculate_lowest_risk(test_file_path, True)
    assert test_first_answer == 16

    # Test input
    test_file_path = get_input_path("15.txt", test=True)

    test_first_answer = calculate_lowest_risk(test_file_path, True)
    assert test_first_answer == 40
    test_second_answer = calculate_lowest_risk(test_file_path, False)
    assert test_second_answer == 315

    # Real input
    file_path = get_input_path("15.txt")

    first_answer = calculate_lowest_risk(file_path, True)
    assert first_answer == 687
    second_answer = calculate_lowest_risk(file_path, False)
    assert second_answer == 2957


if __name__ == "__main__":
    main()
