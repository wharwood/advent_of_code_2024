from __future__ import annotations

class grid_node:
    def __init__(self, x: int, y: int, value) -> None:
        self.x = x
        self.y = y
        self.value = value

    def __repr__(self) -> str:
        return f"({self.x},{self.y}) {self.value}"
    
    def __eq__(self, candidate):
        if not isinstance(candidate, grid_node):
            return NotImplemented
        return self.x == candidate.x and self.y == candidate.y and self.value == candidate.value
    
    def __hash__(self):
        return hash((self.x, self.y, self.value))

class grid:
    def __init__(self, nodes: list[grid_node] = []) -> None:
        self.nodes = nodes

    def __str__(self) -> str:
        output = ""
        for j in range(self.get_len_y()):
            for i in range(self.get_len_x()):
                for node in self.nodes:
                    if i == node.x and j == node.y:
                        output += node.value
            output += "\n"
        return output
    
    def __eq__(self, candidate: grid) -> bool:
        if not isinstance(candidate, grid):
            return NotImplemented
        return sorted(self.nodes, key= lambda x: (x.x, x.y, x.value)) == sorted(candidate.nodes, key= lambda x: (x.x, x.y, x.value))

    def make_grid(self, input: list[str]):
        for j in range(len(input)):
            for i in range(len(input[j])):
                self.nodes.append(grid_node(i,j,input[j][i]))

    def get_len_x(self) -> int:
        return max([node.x for node in self.nodes]) - min([node.x for node in self.nodes]) + 1
    
    def get_len_y(self) -> int:
        return max([node.y for node in self.nodes]) - min([node.y for node in self.nodes]) + 1
    
    def get_node(self, x: int, y: int) -> grid_node:
        for node in self.nodes:
            if node.x == x and node.y == y:
                return node
        raise ValueError(f"No node at ({x},{y}).")
    
    def get_nodes_with_value(self, value: str) -> list[grid_node]:
        matches = []
        for node in self.nodes:
            if node.value == value:
                matches.append(node)
        return matches

    def get_neighbors(self, node: grid_node) -> list[grid_node]:
        neighbors = []
        for n in self.nodes:
            if (n.x+1 == node.x or n.x-1 == node.x) and n.y == node.y:
                neighbors.append(n)
            elif (n.y+1 == node.y or n.y-1 == node.y) and n.x == node.x:
                neighbors.append(n)
        return neighbors

    def get_node_up(self, node: grid_node) -> grid_node | None:
        neighbors = self.get_neighbors(node)
        for n in neighbors:
            if n.x == node.x and n.y+1 == node.y:
                return n
        return None
    
    def get_node_down(self, node: grid_node) -> grid_node | None:
        neighbors = self.get_neighbors(node)
        for n in neighbors:
            if n.x == node.x and n.y-1 == node.y:
                return n
        return None
    
    def get_node_right(self, node: grid_node) -> grid_node | None:
        neighbors = self.get_neighbors(node)
        for n in neighbors:
            if n.x-1 == node.x and n.y == node.y:
                return n
        return None
    
    def get_node_left(self, node: grid_node) -> grid_node | None:
        neighbors = self.get_neighbors(node)
        for n in neighbors:
            if n.x+1 == node.x and n.y == node.y:
                return n
        return None
    
    def update_node(self, node: grid_node) -> None:
        for i, n in enumerate(self.nodes):
            if n.x == node.x and n.y == node.y:
                self.nodes[i] = node
                return
        raise ValueError(f"Node at ({node.x}, {node.y}) not found.")

    def swap_nodes(self, node1: grid_node, node2: grid_node):
        index1, index2 = None, None
        for i, n in enumerate(self.nodes):
            if not index1 and n.x == node1.x and n.y == node1.y:
                index1 = i
            if not index2 and n.x == node2.x and n.y == node2.y:
                index2 = i
        if index1 and index2:
            self.nodes[index1],self.nodes[index2] = node2, node1
            return
        else:
            raise ValueError("One or both nodes not found in grid.")