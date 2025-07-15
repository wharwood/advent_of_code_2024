from grid import grid, grid_node
from enum import Enum
from copy import deepcopy

class guard_direction(Enum):
    up = "^"
    down = "v"
    right = ">"
    left = "<"

class guard:
    def __init__(self, node: grid_node) -> None:
        self.node = node
        self.direction: guard_direction = guard_direction(node.value)

    def move(self, input: grid) -> bool:
        direction_functions = self.get_direction_function(input)
        candidate_function = direction_functions[self.direction.value]
        candidate_node = candidate_function(self.node)
        if candidate_node == None:
            return False
        elif is_blocked(candidate_node):
            candidate_function = direction_functions[self.get_right_adjacent().value]
            candidate_node = candidate_function(self.node)
            if candidate_node == None or is_blocked(candidate_node):
                return False
            else:
                self.direction = self.get_right_adjacent()
                self.update_grid(input, grid_node(candidate_node.x, candidate_node.y, self.get_right_adjacent().value))
                return True
        else:
                self.update_grid(input, candidate_node)
                return True

    def update_grid(self, grid: grid, new_position: grid_node) -> None:
        grid.update_node(grid_node(self.node.x, self.node.y, "X"))
        grid.update_node(grid_node(new_position.x, new_position.y, self.direction.value))
        self.node = new_position

    def get_direction_function(self, grid: grid):
        return {
            "^": grid.get_node_up,
            ">": grid.get_node_right,
            "v": grid.get_node_down,
            "<": grid.get_node_left,
        }
    
    def get_right_adjacent(self) -> guard_direction:
        if self.direction == guard_direction.up:
            return guard_direction.right
        if self.direction == guard_direction.right:
            return guard_direction.down
        if self.direction == guard_direction.down:
            return guard_direction.left
        if self.direction == guard_direction.left:
            return guard_direction.up
        raise ValueError("No matched direction.")

def get_guard_position(grid: grid, 
                       guard_chars: list[str] = [guard_direction.up.value,guard_direction.down.value,guard_direction.right.value,guard_direction.left.value]
                       ) -> grid_node:
    guard_positions = []
    for char in guard_chars:
        guard_positions += grid.get_nodes_with_value(char)
    try:
        return guard_positions.pop()
    except IndexError:
        raise ValueError("No guard in grid")
    
def is_blocked(node: grid_node) -> bool:
    return True if node.value == "#" else False

def is_intersection(node: grid_node) -> bool:
    return True if node.value == "X" else False

def do_part_1(input: list[str]):
    map = grid()
    map.make_grid(input)
    new_position = get_guard_position(map)
    my_guard = guard(new_position)
    guard_moves = [(new_position.x, new_position.y)]
    while my_guard.move(map):
        guard_moves.append((my_guard.node.x, my_guard.node.y))
        print(map)
    print(len(set(guard_moves)))

def do_part_2(input: list[str]):
    pass