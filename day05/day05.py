import math

class Instruction:
    def __init__(self, instruction_list: list[int]):
        self.first_page = int(instruction_list[0])
        self.second_page = int(instruction_list[1])

    def is_in_update(self, update: list[int]) -> bool:
        if not self.first_page in update:
            return False
        if not self.second_page in update:
            return False
        return True

    def is_in_order(self, update: list[int]) -> bool:
        if not self.first_page in update or not self.second_page in update:
            raise ValueError
        first_index = update.index(self.first_page)
        second_index = update.index(self.second_page)
        if first_index < second_index:
            return True
        else:
            return False

    def get_first_index(self, update: list[int]) -> int:
        return update.index(self.first_page)

    def get_second_index(self, update: list[int]) -> int:
        return update.index(self.second_page)

def parseInput(lines):
    instructions = []
    updates = []
    sep = False
    for line in lines:
        if line == '':
            sep = True
            continue
        if sep:
            split = line.split(',')
            updates.append([int(num) for num in split])
        else:
            split = line.split('|')
            instructions.append(Instruction(split))
    return [instructions, updates]

def get_correct_updates(instructions: list[Instruction], updates: list[list[int]]):
    correct_updates = []
    for update in updates:
        for instruction in instructions:
            if not instruction.is_in_update(update):
                continue
            elif not instruction.is_in_order(update):
                break
        else:
            correct_updates.append(update)
    return correct_updates

def get_sum_middles(updates: list[list[int]]) -> int:
    return sum([update[math.floor(len(update)/2)] for update in updates])

def get_instruction_domain(instructions: list[Instruction]) -> list[int]:
    domain = set()
    for instruction in instructions:
            domain.add(instruction.first_page)
            domain.add(instruction.second_page)
    return list(domain)

def get_correct_order(instructions: list[Instruction]):
    ## Define the domain
    domain = get_instruction_domain(instructions)
    ## Instructions are a combination of all possible pages in the domain.
    # The first page will not appear in the second page list and will appear in the first page list n - 1 times where n is the number of items in the domain
    first_pages = []
    for instruction in instructions:
        first_pages.append(instruction.first_page)
    counts = []
    for elem in domain:
        counts.append((elem, first_pages.count(elem)))
    counts = sorted(counts, key= lambda tup: tup[1], reverse=True)
    return [elem[0] for elem in counts]

def is_correct_update(update: list[int], correct_order: list[int]) -> bool:
    correct_update = [elem for elem in correct_order if elem in update]
    if update == correct_update:
        return True
    else:
        return False
    
def do_correct_update(update: list[int], correct_order: list[int]) -> list[int]:
    return [list for list in correct_order if list in update]

def get_relevant_instructions(instructions: list[Instruction], update: list[int]) -> list[Instruction]:
    return [instruction for instruction in instructions if instruction.is_in_update(update)]

def do_part_1(input):
    data = parseInput(input)
    instructions = data[0]
    updates = data[1]
    sum_middles = 0
    correct_updates = get_correct_updates(instructions, updates)
    if not correct_updates == None:
        sum_middles = sum([update[math.floor(len(update)/2)] for update in correct_updates])
    print (sum_middles)

def do_part_2(input):
    data = parseInput(input)
    instructions = data[0]
    updates = data[1]
    corrected_updates = []
    for update in updates:
        relavant_instructions = get_relevant_instructions(instructions, update)
        correct_order = get_correct_order(relavant_instructions)
        if not is_correct_update(update, correct_order):
            corrected_updates.append(do_correct_update(update, correct_order))
    print(get_sum_middles(corrected_updates))