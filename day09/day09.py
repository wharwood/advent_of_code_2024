from __future__ import annotations
from enum import Enum

class block:
    def __init__(self, start_index: int, size: int):
        self.start_index = start_index
        self.size = size
    
    def __repr__(self):
        representation = str(self.start_index) + ': '
        for n in range(self.size):
            representation += "."
        return representation

class file(block):
    def __init__(self, id: int, start_index: int, size: int):
        super().__init__(start_index, size)
        self.id = id

    def split(self, size: int) -> tuple[file, file]:
        return (file(self.id, self.start_index, self.size - size), 
                file(self.id, self.start_index + self.size - size, size))
    
    def __repr__(self):
        representation = str(self.start_index) + ': '
        for n in range(self.size):
            representation += str(self.id)
        return representation

class file_system:
    def __init__(self, input: str):
        self.blocks = self.initialize_blocks(input)

    def __repr__(self):
        representation = ''
        sorted_blocks = sorted(self.blocks, key= lambda x: x.start_index)
        for block in sorted_blocks:
            for n in range(block.size):
                representation += str(block.id % 10) if isinstance(block, file) else '.'
        return representation
        
    def initialize_blocks(self, raw: str) -> list[block]:
        blocks = []
        id_count = 0
        index = 0
        for n in range(len(raw)):
            if n % 2 == 0:
                blocks.append(file(id_count, index, int(raw[n])))
                id_count += 1
            else:
                if not int(raw[n]) == 0:
                    blocks.append(block(index, int(raw[n])))
            index += int(raw[n])
        return blocks
    
    def get_leftmost_free(self) -> block:
        return min([block for block in self.blocks if not isinstance(block, file)], key= lambda x: x.start_index)
    
    def get_rightmost_file(self) -> file:
        return max([block for block in self.blocks if isinstance(block, file)], key= lambda x: x.start_index)
    
    def split_file_by_size(self, file: file, size: int) -> None:
        if file not in self.blocks:
            raise ValueError("File not found in the file system.")
        elif size <= 0 or size >= file.size:
            raise ValueError("Invalid size for splitting the file.")
        else:
            file1, file2 = file.split(size)
            self.blocks.remove(file)
            self.blocks.append(file1)
            self.blocks.append(file2)

    def fill_leftmost_free(self) -> None:
        leftmost_free = self.get_leftmost_free()
        rightmost_file = self.get_rightmost_file()
        if leftmost_free.size == rightmost_file.size:
            rightmost_file.start_index = leftmost_free.start_index
            self.blocks.remove(leftmost_free)
        elif leftmost_free.size > rightmost_file.size:
            rightmost_file.start_index = leftmost_free.start_index
            leftmost_free.start_index += rightmost_file.size
            leftmost_free.size -= rightmost_file.size

    def fragmented_compress(self) -> None:
        while not max([block.start_index for block in self.blocks if isinstance(block, file)]) < min([block.start_index for block in self.blocks if not isinstance(block, file)]):
            leftmost_free = self.get_leftmost_free()
            rightmost_file = self.get_rightmost_file()
            if leftmost_free.size < rightmost_file.size:
                self.split_file_by_size(rightmost_file, leftmost_free.size)
                continue
            elif leftmost_free.size == rightmost_file.size:
                rightmost_file.start_index = leftmost_free.start_index
                self.blocks.remove(leftmost_free)
            elif leftmost_free.size > rightmost_file.size:
                rightmost_file.start_index = leftmost_free.start_index
                leftmost_free.start_index += rightmost_file.size
                leftmost_free.size -= rightmost_file.size

    def compress(self) -> None:
        self.blocks.sort(key=lambda x: x.start_index)
        files = [block for block in self.blocks if isinstance(block, file)]
        files.sort(key=lambda x: x.start_index, reverse=True)
        for f in files:
            for b in self.blocks:
                if not isinstance(b, file) and b.start_index < f.start_index and b.size >= f.size:
                    if b.size == f.size:
                        f.start_index = b.start_index
                        self.blocks.remove(b)
                        break
                    elif b.size > f.size:
                        f.start_index = b.start_index
                        b.start_index += f.size
                        b.size -= f.size
                        break

    def checksum(self) -> int:
        checksum = 0
        for block in self.blocks:
            if not isinstance(block, file) or block.size == 0:
                continue
            for n in range(block.size):
                checksum += block.id * (block.start_index + n)
        return checksum
    
def do_part_1(input: list[str]):
    for line in input:
        fs = file_system(line.strip())
        fs.fragmented_compress()
        print(fs.checksum())

def do_part_2(input: list[str]):
    for line in input:
        fs = file_system(line.strip())
        fs.compress()
        print(fs.checksum())