input_path = "./input.txt"


def read_input(path):
    with open(path, "r") as file:
        return [line.strip() for line in file.readlines()]


def find_highest_value(s):
    # Part 1
    l = 0
    res = 0
    for r in range(1, len(s)):
        res = max(res, int(s[l] + s[r]))
        if int(s[r]) > int(s[l]):
            l = r
    return res


def backtrack_find_highest_value(s):
    maxV = 0

    subset = []

    def dfs(i):
        nonlocal maxV
        if i >= len(s):
            if len(subset) == 12:
                v = "".join(subset)
                maxV = max(maxV, int(v))
            return
        # print(subset)
        # Include the value
        subset.append(s[i])
        dfs(i + 1)
        subset.pop()

        # Skip this value
        dfs(i + 1)

    dfs(0)

    return maxV


if __name__ == "__main__":
    lines = read_input(input_path)
    finalSum = 0
    for line in lines:
        # v = find_highest_value(str(line))
        v = backtrack_find_highest_value(str(line))
        print(v)
        finalSum += v

    print(finalSum)
