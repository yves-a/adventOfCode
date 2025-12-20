# read the input from file and put it into a 2d array
def read_input(path):
    with open(path, "r") as file:
        return [line.strip() for line in file.readlines()]


def check_input(grid, row, col):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    count = 0
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            if grid[r][c] == "@":
                count += 1
    return count < 4


if __name__ == "__main__":
    input_data = [list(row) for row in read_input("./input.txt")]
    res = 0
    prevRes = -1
    while res != prevRes:
        prevRes = res
        for r in range(len(input_data)):
            for c in range(len(input_data[0])):
                if input_data[r][c] == "@":
                    if check_input(input_data, r, c):
                        input_data[r][c] = "x"
                        res += 1

    print(res)
