import re

class mult_command:
    def __init__(self, raw: str) -> None:
        self.raw = raw
        self.mults: list[tuple[int, int]] = self.get_mults()
    
    def get_mults(self):
        on = True
        mults = list()
        commands = re.findall(r"mul\(\d+,\d+\)|don't\(\)|do\(\)", self.raw)
        for command in commands:
            if command == "don't()":
                on = False
            elif command == "do()":
                on = True
            elif not on:
                continue
            else:
                digits = re.findall(r"(\d+)",command)
                if len(digits) == 2:
                    mults.append((int(digits[0]),int(digits[1])))
        return mults
    
    def get_total(self):
        result = 0
        for mult in self.mults:
            result += mult[0] * mult[1]
        return result

def do_part_1(input: list[str]):
    command = mult_command(input[0])
    print(command.get_total())