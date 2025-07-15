from grid import grid, grid_node
from enum import Enum
from copy import deepcopy

class guard_direction(Enum):
    up = "^"
    down = "v"
    right = ">"
    left = "<"

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
    
def get_right_adjacent(direction: guard_direction | str) -> guard_direction:
    if isinstance(direction, str):
        direction = guard_direction(direction)
    if direction == guard_direction.up:
        return guard_direction.right
    if direction == guard_direction.right:
        return guard_direction.down
    if direction == guard_direction.down:
        return guard_direction.left
    if direction == guard_direction.left:
        return guard_direction.up
    raise ValueError("No matched direction.")

def move_guard(input: grid) -> grid_node | None:
    guard_node = get_guard_position(input)
    direction_functions = {
        "^": input.get_node_up,
        ">": input.get_node_right,
        "v": input.get_node_down,
        "<": input.get_node_left
    }
    candidate_function = direction_functions[guard_node.value]
    candidate_node = candidate_function(guard_node)
    if candidate_node == None:
        return None
    elif is_blocked(candidate_node):
        candidate_function = direction_functions[get_right_adjacent(guard_node.value).value]
        candidate_node = candidate_function(guard_node)
        if candidate_node == None or is_blocked(candidate_node):
            return None
        else:
            return grid_node(candidate_node.x, candidate_node.y, get_right_adjacent(guard_node.value).value)
    else:
            return grid_node(candidate_node.x, candidate_node.y, guard_node.value)
    return None

def is_blocked(node: grid_node) -> bool:
    return True if node.value == "#" else False

def do_part_1(input: list[str]):
    map = grid()
    map.make_grid(input)
    new_position = get_guard_position(map)
    guard_moves = [(new_position.x, new_position.y)]
    while True:
        new_position = move_guard(map)
        if new_position is None:
            break
        old_position = map.get_node(guard_moves[-1][0], guard_moves[-1][1])
        map.update_node(grid_node(old_position.x, old_position.y, "X"))
        map.update_node(new_position)
        guard_moves.append((new_position.x, new_position.y))
        ## print(map)
    print(len(set(guard_moves)))