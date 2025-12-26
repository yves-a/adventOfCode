def readInput(filePath):
    with open(filePath, "r") as file:
        lines = file.readlines()

    split_lines = [line.strip().split(" ") for line in lines]
    adj = {}
    for line in split_lines:
        adj[line[0].split(":")[0]] = line[1:]

    return adj


def countPaths(adj):
    # Part 1
    count = 0
    visited = set()

    def dfs(n):
        nonlocal count
        if n == "out":
            count += 1
            return

        visited.add(n)
        for neigh in adj[n]:
            dfs(neigh)
        visited.remove(n)

    dfs("you")
    return count


def countPathsWithDP(adj, start_node, end_node, req_a, req_b):
    memo = {}

    def solve(u, mask):
        # Use bitmasking to set flags when passing required nodes
        new_mask = mask
        if u == req_a:
            new_mask |= 1
        if u == req_b:
            new_mask |= 2

        # Check if reached the end node we also need to have visited both required nodes
        if u == end_node:
            return 1 if new_mask == 3 else 0

        state = (u, new_mask)
        if state in memo:
            return memo[state]

        # Sum paths from current node to end node
        total_paths = 0
        for v in adj[u]:
            total_paths += solve(v, new_mask)

        memo[state] = total_paths
        return total_paths

    return solve(start_node, 0)


if __name__ == "__main__":
    adj = readInput("./input.txt")
    # Part 1
    # print(countPaths(adj))
    result = countPathsWithDP(adj, "svr", "out", "fft", "dac")
    print(result)
