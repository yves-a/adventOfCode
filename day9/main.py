def readInput(file_path):
    with open(file_path, "r") as file:
        data = file.readlines()
    return [[int(x) for x in line.strip().split(",")] for line in data]


def bruteForceArea(points):
    # Part 1
    maxArea = 0
    maxPoints = (None, None)
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            area = (abs(points[i][0] - points[j][0]) + 1) * (
                abs(points[i][1] - points[j][1]) + 1
            )
            if area > maxArea:
                maxArea = area
                maxPoints = (points[i], points[j])
    return maxArea, maxPoints


def createGrid(points):
    # Basic idea is to sort the x and y coordinates, and create a smaller grid based on their indices
    # So instead of 100k by 100k grid, we can have a 500 by 500 grid if there are 500 unique x and y coordinates

    # 100k by 100k grid would be too large to handle directly

    # Just look up the real coordinates when needed using the mapping

    # Coordinate compression
    sorted_x = sorted(list(set(p[0] for p in points)))
    sorted_y = sorted(list(set(p[1] for p in points)))

    x_map = {x: i for i, x in enumerate(sorted_x)}
    y_map = {y: i for i, y in enumerate(sorted_y)}

    # Make the grid smaller than the actual coordinates
    grid = [[0 for _ in range(len(sorted_x))] for _ in range(len(sorted_y))]

    # Find the vertical lines, so that once you pass them, you can switch the fill on or off
    vertical_edges = set()

    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]

        ix1, iy1 = x_map[p1[0]], y_map[p1[1]]
        ix2, iy2 = x_map[p2[0]], y_map[p2[1]]
        # Vertical line
        if ix1 == ix2:
            for iy in range(min(iy1, iy2), max(iy1, iy2) + 1):
                grid[iy][ix1] = 1
            for iy in range(min(iy1, iy2), max(iy1, iy2)):
                vertical_edges.add((ix1, iy))
        # Horizontal line
        else:
            for ix in range(min(ix1, ix2), max(ix1, ix2) + 1):
                grid[iy1][ix] = 1

    # Fill the area
    for i in range(len(grid)):
        switch = False
        for j in range(len(grid[0])):
            if (j, i) in vertical_edges:
                switch = not switch
            if switch or grid[i][j] == 1:
                grid[i][j] = 1

    return grid, x_map, y_map


def buildPrefixSum(grid):
    rows = len(grid)
    cols = len(grid[0])
    prefix_sum = [[0] * (cols + 1) for _ in range(rows + 1)]
    # Have an extra row and column to handle boundaries and to avoid index errors
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            prefix_sum[i][j] = (
                grid[i - 1][j - 1]
                + prefix_sum[i - 1][j]
                + prefix_sum[i][j - 1]
                - prefix_sum[i - 1][j - 1]
            )
    return prefix_sum


def findLargestAreaInGrid(prefix_sum, points, x_map, y_map):
    max_area = 0
    max_points = (None, None)
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, y1 = points[i]
            x2, y2 = points[j]

            # Get the smaller compressed grid indices
            ix1, iy1 = x_map[x1], y_map[y1]
            ix2, iy2 = x_map[x2], y_map[y2]

            ps_x1, ps_y1 = min(ix1, ix2) + 1, min(iy1, iy2) + 1
            ps_x2, ps_y2 = max(ix1, ix2) + 1, max(iy1, iy2) + 1

            area = (
                prefix_sum[ps_y2][ps_x2]
                - prefix_sum[ps_y1 - 1][ps_x2]
                - prefix_sum[ps_y2][ps_x1 - 1]
                + prefix_sum[ps_y1 - 1][ps_x1 - 1]
            )

            expected_area = (abs(ix1 - ix2) + 1) * (abs(iy1 - iy2) + 1)

            if area == expected_area:
                # Find the actual area in original coordinates
                area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
                if area > max_area:
                    max_area = area
                    max_points = (points[i], points[j])
    return max_area, max_points


if __name__ == "__main__":
    input_data = readInput("./input.txt")
    # Part 1
    # area, point_pair = bruteForceArea(input_data)
    # print(f"Maximum Area: {area} between points {point_pair[0]} and {point_pair[1]}")
    grid, x_map, y_map = createGrid(input_data)

    prefix_sum = buildPrefixSum(grid)
    max_area, max_points = findLargestAreaInGrid(prefix_sum, input_data, x_map, y_map)

    print(max_area)
