from grid import grid, grid_node
from enum import Enum

class frequency:
    def __init__(self, symbol: str, grid: grid, antinode_method: str) -> None:
        self.symbol = symbol
        if antinode_method not in frequency.method.__members__:
            raise NotImplementedError(f"Antinode method '{antinode_method}' is not implemented.")
        self.antinode_method = frequency.method[antinode_method]
        self.nodes = []
        self.initialize_nodes(grid)
        self.antinodes = []
        self.initialize_antinodes(grid)

    def initialize_nodes(self, grid: grid):
        for node in grid.nodes:
            if node.value == self.symbol:
                self.nodes.append(node)

    def initialize_antinodes(self, grid: grid):
        antinode_methods = { frequency.method.adjacent: self.get_adjacent_antinodes, 
                            frequency.method.colinear: self.get_colinear_antinodes, }
        method = antinode_methods[self.antinode_method]
        candidates = []
        if not len(self.nodes) < 2:
            for j, node1 in enumerate(self.nodes):
                for i, node2 in enumerate(self.nodes):
                    # Ensure we don't compare nodes with themselves or in reverse order
                    if i > j:
                        new_candidates = method(node1, node2, grid)
                        for new_candidate in new_candidates:
                            if not any(new_candidate == candidate for candidate in candidates):
                                candidates.append(new_candidate)
        self.antinodes = candidates

    @staticmethod
    def get_adjacent_antinodes(node1: grid_node, node2: grid_node, grid: grid) -> list[grid_node]:
        if node1.x == node2.x and node1.y == node2.y:
            raise ValueError("Nodes have the same coordinates.")
        dx = node2.x - node1.x
        dy = node2.y - node1.y
        candidate_coordinates = [(node1.x + dx, node1.y + dy),
                                 (node1.x - dx, node1.y - dy), 
                                 (node2.x + dx, node2.y + dy),
                                 (node2.x - dx, node2.y - dy)]
        antinodes = []
        for x, y in candidate_coordinates:
            if grid.is_in_grid(x, y) and x != node1.x and y != node1.y and x != node2.x and y != node2.y:
                antinodes.append(grid.get_node(x, y))
        return antinodes
    
    @staticmethod
    def get_colinear_antinodes(node1: grid_node, node2: grid_node, grid: grid) -> list[grid_node]:
        if node1.x == node2.x and node1.y == node2.y:
            raise ValueError("Nodes have the same coordinates.")
        antinodes = []
        dx = node2.x - node1.x
        dy = node2.y - node1.y
        for node in grid.nodes:
            if (node.x - node1.x) * dy == (node.y - node1.y) * dx:
                antinodes.append(node)
        return antinodes
    
    class method(Enum):
        adjacent = "adjacent"
        colinear = "colinear"

def do_part_1(input):
    map = grid()
    map.make_grid(input)
    frequencies: list[frequency] = []
    for node in map.nodes:
        if not node.value == "." and not any(freq.symbol == node.value for freq in frequencies):
            frequencies.append(frequency(node.value, map, "adjacent"))
    antinodes = set()
    for freq in frequencies:
        antinodes.update(freq.antinodes)
    print(len(antinodes))
    print(grid(list(antinodes)))

def do_part_2(input):
    map = grid()
    map.make_grid(input)
    frequencies: list[frequency] = []
    for node in map.nodes:
        if not node.value == "." and not any(freq.symbol == node.value for freq in frequencies):
            frequencies.append(frequency(node.value, map, "colinear"))
    antinodes = set()
    for freq in frequencies:
        antinodes.update(freq.antinodes)
    print(len(antinodes))
    print(grid(list(antinodes)))