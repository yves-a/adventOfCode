input_path = "./input.txt"


def read_input(path):
    with open(path, "r") as file:
        return [line.strip() for line in file.readlines()]


def handle_input(lines):
    # Part 1 & 2
    res = 0
    curr = 50

    for line in lines:
        turn = line[0]
        value = int(line[1:])

        multiple_passes = value // 100

        value = value % 100

        prev = curr

        if turn == "L":
            curr -= value
        elif turn == "R":
            curr += value

        if curr < 0:
            curr += 100
            if prev != 0 and curr != 0:
                res += 1 if prev != 0 else 0
        elif curr > 99:
            curr -= 100
            if prev != 0 and curr != 0:
                res += 1 if prev != 0 else 0

        if curr == 0:
            res += 1

        res += multiple_passes

    return res


if __name__ == "__main__":
    lines = read_input(input_path)
    print(handle_input(lines))
