from collections import deque
import numpy as np
from scipy.optimize import linprog


def readInput(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Multiple lines of input, each line contains light configuration and buttons
    res = []
    for line in lines:
        line = line.strip().split(" ")
        buttons = []
        lights = {}
        button = ()
        joltage = set()
        for i, ch in enumerate(line[0].split("[")[-1].split("]")[0]):
            if ch != "]" or ch != "[":
                lights[i] = ch == "#"
        for item in line[1:]:
            if item.startswith("("):
                button = list(int(x) for x in item[1:-1].split(","))
                buttons.append(button)
            elif item.startswith("{"):
                joltage = list(int(x) for x in item[1:-1].split(","))
        res.append((lights, buttons, joltage))

    return res


def findMinClicksWithBFS(lights, buttons):
    # Part 1
    target = tuple(lights.values())
    initial = tuple(False for _ in lights)

    queue = deque()
    queue.append((initial, 0))
    visited = set()
    visited.add(initial)

    while queue:
        state, clicks = queue.popleft()
        if state == target:
            return clicks
        for button in buttons:
            new_state = list(state)
            for idx in button:
                new_state[idx] = not new_state[idx]
            new_state_tuple = tuple(new_state)
            if new_state_tuple not in visited:
                visited.add(new_state_tuple)
                queue.append((new_state_tuple, clicks + 1))

    return -1


def findMinClicksForJoltageWithGaussianElimination(buttons, joltage):
    # Convert joltage and buttons to an numpy array system
    n = len(joltage)
    A = np.zeros((n, len(buttons)), dtype=int)
    b = np.array(list(joltage), dtype=int)
    for j, button in enumerate(buttons):
        for idx in button:
            A[idx][j] += 1

    c = np.ones(len(buttons))

    # All variables must be integers (0 or more clicks)
    integrality = np.ones(len(buttons))

    res = linprog(
        c, A_eq=A, b_eq=b, bounds=(0, None), integrality=integrality, method="highs"
    )

    return int(np.sum(np.round(res.x)))


if __name__ == "__main__":
    inputs = readInput("./input.txt")
    totalMinClicks = 0
    for lights, buttons, joltage in inputs:
        # Part 1
        # min_clicks = findMinClicksWithBFS(lights, buttons)
        min_clicks = findMinClicksForJoltageWithGaussianElimination(buttons, joltage)
        print("Minimum clicks:", min_clicks)
        totalMinClicks += min_clicks
    print("Total minimum clicks:", totalMinClicks)
