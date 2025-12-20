# Make the merge the intervals
def mergeIntervals(intervals):

    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = []
    for current in sorted_intervals:
        if not merged or merged[-1][1] < current[0]:
            # New interval
            merged.append(current)
        else:
            merged[-1][1] = max(merged[-1][1], current[1])

    return merged


def readInput(file_path):
    intervals = []
    ids = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        reading_intervals = True
        for line in lines:
            line = line.strip()
            if line == "":
                reading_intervals = False
                continue
            if reading_intervals:
                start, end = map(int, line.split("-"))
                intervals.append([start, end])
            else:
                ids.append(int(line))
    return intervals, ids


def checkFresh(intervals, id):
    for start, end in intervals:
        if id >= start and id <= end:
            return True

    return False


if __name__ == "__main__":
    intervals, ids = readInput("./input.txt")

    merged_intervals = mergeIntervals(intervals)
    res = 0
    # Part 1
    # for id in ids:
    #     if checkFresh(intervals, id):
    #         res += 1

    total_res = 0
    for start, end in merged_intervals:
        total_res += end - start + 1

    print(total_res)
