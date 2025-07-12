def parseInput(input: list[str]):
    reports = list()
    for line in input:
        report = line.split()
        reports.append([int(item) for item in report])
    return reports

def isMonotonic(report: list):
    copy = report.copy()
    if copy[1] < copy[0]:
        copy.reverse()
    for n in range(1,len(copy)):
        if copy[n] > copy[n-1]:
            continue
        else:
            return False
    return True

def isClose(report: list, high: int = 3, low: int = 1):
    for n in range(1,len(report)):
        if abs(report[n] - report[n-1]) > high or abs(report[n] - report[n-1]) < low:
            return False
    return True

def do_part_1(input):
    reports = parseInput(input)
    safeReports = list()
    for n in range(len(reports)):
        if isMonotonic(reports[n]) and isClose(reports[n]):
            safeReports.append(reports[n])
    print(len(safeReports))

def do_part_2(input):
    reports = parseInput(input)
    safeReports = list()
    for n in range(len(reports)):
        if isMonotonic(reports[n]) and isClose(reports[n]):
            safeReports.append(reports[n])
        else:
            for i in range(len(reports[n])):
                modReport = reports[n].copy()
                modReport.pop(i)
                if isMonotonic(modReport) and isClose(modReport):
                    safeReports.append(reports[n])
                    break
    print(len(safeReports))