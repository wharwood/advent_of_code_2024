class calibration:
    def __init__(self, total: int, elements: list[int], operations: list[str]) -> None:
        self.total = total
        self.elements = elements
        self.operations = operations

    def __repr__(self) -> str:
        return f"{self.total}: {self.elements}"

    def is_operable(self) -> bool:
        operation_map = {
            "add": self.add,
            "multiply": self.multiply,
            "concatenate": self.concatenate
        }
        if len(self.elements) < 1:
            raise ValueError
        elif len(self.elements) == 1:
            return True if self.total == self.elements[0] else False
        else:
            for operation in self.operations:
                if operation_map[operation]():
                    return True
        return False
    
    def add(self):
        new_elements = [self.elements[0] + self.elements[1]]
        new_elements += self.elements[2:]
        new_calibration = calibration(self.total, new_elements, self.operations)
        if new_calibration.is_operable():
            return True
        
    def multiply(self):
        new_elements = [self.elements[0] * self.elements[1]]
        new_elements += self.elements [2:]
        new_calibration = calibration(self.total, new_elements, self.operations)
        if new_calibration.is_operable():
            return True
        
    def concatenate(self):
        new_elements = [int(str(self.elements[0])+str(self.elements[1]))]
        new_elements += self.elements [2:]
        new_calibration = calibration(self.total, new_elements, self.operations)
        if new_calibration.is_operable():
            return True

def do_part_1(input: list[str]):
    calibrations: list[calibration] = []
    for line in input:
        total, elements = line.split(": ")
        calibrations.append(calibration(int(total), [int(i) for i in elements.split(" ")], ["add", "multiply"]))
    print(sum([i.total for i in calibrations if i.is_operable()]))

def do_part_2(input: list[str]):
    calibrations: list[calibration] = []
    for line in input:
        total, elements = line.split(": ")
        calibrations.append(calibration(int(total), [int(i) for i in elements.split(" ")], ["add", "multiply", "concatenate"]))
    print(sum([i.total for i in calibrations if i.is_operable()]))