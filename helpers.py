class helpers:

    @staticmethod
    def parse_input(file: str) -> list[str]:
        fp = open(file)
        return [line.rstrip() for line in fp.readlines()]