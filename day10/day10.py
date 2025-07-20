from __future__ import annotations
from grid import grid, grid_node

class trailhead(grid_node):
    def __init__(self, x: int, y: int, value: int):
        super().__init__(x, y, value)

    def get_score(self, map: map) -> int:
        candidates = set([self])
        for i in range(1,10):
            new_candidates = set()
            while candidates:
                new_candidates.update([n for n in map.get_neighbors(candidates.pop()) if n.value == i])
            candidates = new_candidates
        return len(candidates)
    
    def get_rating(self, map: map) -> int:
        def dfs(node: grid_node, value: int):
            if node.value == 9:
                return 1
            count = 0
            for neighbor in map.get_neighbors(node):
                if neighbor.value == value + 1:
                    count += dfs(neighbor, neighbor.value)
            return count
        return dfs(self, self.value)

class map(grid):
    def __init__(self, input: list[str]):
        super().__init__()
        self.make_grid(input)
        self.change_values_type(int)
        self.trailheads = self.initialize_trailheads()

    def initialize_trailheads(self) -> list[trailhead]:
        trailheads = []
        nodes_to_remove = []
        for node in self.nodes:
            if not isinstance(node, trailhead) and node.value == 0:
                nodes_to_remove.append(node)
                trailheads.append(trailhead(node.x, node.y, 0))
        for node in nodes_to_remove:
            self.nodes.remove(node)
        self.nodes += trailheads
        return trailheads
    
    def get_total_score(self) -> int:
        total = 0
        for node in self.nodes:
            if isinstance(node, trailhead):
                total += node.get_score(self)
        return total
    
    def get_total_rating(self) -> int:
        total_rating = 0
        for node in self.nodes:
            if isinstance(node, trailhead):
                total_rating += node.get_rating(self)
        return total_rating

def do_part_1(input: list[str]):
    trail_map = map(input)
    print(trail_map.get_total_score())

def do_part_2(input: list[str]):
    trail_map = map(input)
    print(trail_map.get_total_rating())