def makeCandidates(input: list[str]):
    ## Horizontal
    candidates = input.copy()
    ## Vertical
    for n in range(len(input)):
        temp = ""
        for elem in input:
            temp += elem[n]
        candidates.append(temp)
    ## Forward Diagonal
    candidates.extend(makeDiagCandidates(input))
    return candidates

def makeDiagCandidates(input: list[str]):
    directions = [True, False]
    candidates = []
    for direction in directions:
        starts = []
        for i in range(len(input[0])):
            starts.append((i,0))
        for j in range(1,len(input)):
            if direction:
                starts.append((0,j))
            else:
                starts.append((len(input[0])-1,j))
        for start in starts:
            temp = ''
            coordinate = start
            while coordinate[0] < len(input[0]) and coordinate[0] >= 0 and coordinate[1] < len(input):
                temp += (input[coordinate[1]][coordinate[0]])
                if direction:
                    coordinate = (coordinate[0]+1,coordinate[1]+1)
                else:
                    coordinate = (coordinate[0]-1,coordinate[1]+1)
            candidates.append(temp)
    return candidates

def findXMAS(candidates: list[str]):
    return sum([candidate.count('XMAS') + candidate.count('SAMX') for candidate in candidates])

def do_part_1(input):
    candidates = makeCandidates(input)
    occurances = findXMAS(candidates)
    print(occurances)

KERNALS = [['M.M','.A.','S.S'],['M.S','.A.','M.S'],['S.S','.A.','M.M'],['S.M','.A.','S.M']]

def kernelComp(input: list[str], kernel: list[str], ignoreChar: str = '.') -> bool:
    if not len(input) == len(kernel):
        raise ValueError
    elif not len(input[0]) == len(kernel[0]):
        raise ValueError
    for j in range(len(input)):
        for i in range(len(input[0])):
            if not kernel[j][i] == '.':
                if not input[j][i] == kernel[j][i]:
                    return False
    return True

def countKernels(input: list[str], kernels: list[list[str]]) -> int:
    result = 0
    for kernel in kernels:
        for j in range(len(input)-len(kernel)+1):
            for i in range(len(input[0])-len(kernel[0])+1):
                candidate = []
                for row in input[j:j+len(kernel)]:
                    candidate.append(row[i:i+len(kernel[0])])
                if kernelComp(candidate, kernel):
                    result += 1
    return result

def do_part_2(input):
    print(countKernels(input, KERNALS))