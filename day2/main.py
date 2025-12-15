input_path = "./input.txt"


def read_input(path):
    with open(path, "r") as file:
        # 1 line but comma separated ranges
        line = file.readline().strip()
        parts = line.split(",")
        return parts


def find_all_invalid_between(start, end):
    total = 0
    pattern_found = False
    for i in range(start, end + 1):
        string_i = str(i)
        len_i = len(string_i)
        # check for all k partitions
        for k in range(2, len_i + 1):
            pattern_found = equal_paritions(string_i, k)
            if pattern_found:
                break

        if pattern_found:
            total += i
            pattern_found = False

    return total


def equal_paritions(s, k):
    # check if s can be partitioned into k equal parts
    n = len(s)

    if n % k != 0:
        return False

    length = n // k
    prev = None
    pattern = True

    # check each partition if it is equal to prev
    for i in range(0, n, length):
        if prev is not None:
            pattern = prev == s[i : i + length]

        prev = s[i : i + length]

        if not pattern:
            return False

    return True


if __name__ == "__main__":
    lines = read_input(input_path)
    res = 0
    for line in lines:
        parts = line.split("-")
        start = int(parts[0])
        end = int(parts[1])
        res += find_all_invalid_between(start, end)
    print(res)
