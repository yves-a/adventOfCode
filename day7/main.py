from collections import defaultdict, deque


def readInput(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return [list(line.strip()) for line in lines]


def solveGraph(graph):
    # Part 1
    splitCount = 0

    def dfs(row, col, visited):
        nonlocal splitCount
        if (
            (row, col) in visited
            or row not in range(len(graph))
            or col not in range(len(graph[0]))
        ):
            return

        visited.add((row, col))

        if graph[row][col] == ".":
            graph[row][col] = "|"
            dfs(row + 1, col, visited)
        elif graph[row][col] == "^":
            splitCount += 1
            dfs(row, col + 1, visited)
            dfs(row, col - 1, visited)

        return

    for i in range(len(graph[0])):
        if graph[0][i] == "S":
            dfs(1, i, set())

    return splitCount


def findStartNode(graph):
    for i in range(len(graph[0])):
        if graph[0][i] == "S":
            return (0, i)


def countPaths(graph, startNode):
    R = len(graph)
    C = len(graph[0])

    counts = [[0 for _ in range(C)] for _ in range(R)]
    counts[startNode[0]][startNode[1]] = 1

    for r in range(startNode[0], R):
        for c in range(C):
            if counts[r][c] == 0:
                continue

            if graph[r][c] == "." or graph[r][c] == "S":
                if r + 1 < R:
                    counts[r + 1][c] += counts[r][c]

            elif graph[r][c] == "^":
                if r + 1 < R:
                    if c - 1 >= 0:
                        counts[r + 1][c - 1] += counts[r][c]
                    if c + 1 < C:
                        counts[r + 1][c + 1] += counts[r][c]

    return sum(counts[-1])


if __name__ == "__main__":
    graph = readInput("./input.txt")
    # print(solveGraph(graph))
    startNode = findStartNode(graph)
    counts = countPaths(graph, startNode)
    print(counts)
    # for key in adj:
    #     print(f"{key}: {adj[key]}")
