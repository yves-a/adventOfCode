import math
import heapq


def readInput(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return [[int(x) for x in line.strip().split(",")] for line in lines]


def bruteForceCombining(nodes):
    parent = {}
    min_heap = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if i != j:
                distance = math.dist(nodes[i], nodes[j])
                heapq.heappush(min_heap, (distance, nodes[i], nodes[j]))

    parent = {tuple(node): tuple(node) for node in nodes}
    sizes = {tuple(node): 1 for node in nodes}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            if sizes[rootX] < sizes[rootY]:
                rootX, rootY = rootY, rootX
            parent[rootY] = rootX
            sizes[rootX] += sizes[rootY]
            return True
        return False

    # Part 1
    # count = 999
    print(len(min_heap))
    groups = len(nodes)
    lastPair = None
    while groups > 1:
        distance, a, b = heapq.heappop(min_heap)
        if union(tuple(a), tuple(b)):
            lastPair = (a, b, distance)
            groups -= 1
        # Part 1
        # count -= 1

    # Return the sizes but sorted
    sizes_list = sorted(sizes.values(), reverse=True)

    return sizes_list, lastPair


def multiplyLargestGroups(sizes, n=3):
    # Part 1
    result = 1

    print("Sizes:", sizes)
    for i in range(min(n, len(sizes))):
        print(f"Group {i+1} size: {sizes[i]}")
        result *= sizes[i]
    return result


if __name__ == "__main__":
    nodes = readInput("input.txt")
    sizes, lastPair = bruteForceCombining(nodes)
    result = multiplyLargestGroups(sizes, 3)

    print("Last pair x coordinates combined:", lastPair[0][0] * lastPair[1][0])
