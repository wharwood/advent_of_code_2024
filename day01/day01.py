def do_part_1(input):
    list1 = list()
    list2 = list()
    for line in input:
        elements = line.split()
        list1.append(int(elements[0]))
        list2.append(int(elements[1]))
    list1.sort()
    list2.sort()
    result = 0
    for i in range(len(list1)):
        result += abs(list1[i]-list2[i])
    print(result)

def do_part_2(input):
    list1 = list()
    list2 = list()
    for line in input:
        elements = line.split()
        list1.append(int(elements[0]))
        list2.append(int(elements[1]))
    list1.sort()
    list2.sort()
    result = sum([list2.count(elem)*elem for elem in list1])
    print(result)