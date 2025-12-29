def readInput(filePath):
    with open(filePath, "r") as file:
        lines = file.readlines()
    shape_dict = {}
    check = []
    lineIndex = 0
    while lineIndex < len(lines):
        line = lines[lineIndex]
        cleaned_line = line.strip()
        if cleaned_line and cleaned_line[0].isdigit() and cleaned_line[-1] == ":":
            key = int(cleaned_line[:-1])
            shape = []
            for y in range(3):
                lineIndex += 1
                formatted_line = lines[lineIndex].strip()
                for x in range(3):
                    if formatted_line[x] == "#":
                        shape.append((x, y))
            shape_dict[key] = shape

        elif cleaned_line and "x" in cleaned_line and ":" in cleaned_line:
            dims_part, values_part = cleaned_line.split(":")
            width, height = map(int, dims_part.split("x"))
            values = list(map(int, values_part.strip().split()))
            curr_line = []
            curr_line.append((width, height))
            curr_line.append(values)
            check.append(curr_line)
        lineIndex += 1

    return shape_dict, check


def getAllVariations(shape_coords):
    variations = set()
    # Initial conversion to (r, c)
    curr = [(y, x) for x, y in shape_coords]

    for _ in range(2):  # Flip
        for _ in range(4):  # Rotate
            # Rotate (r, c) -> (c, -r)
            curr = [(c, -r) for r, c in curr]
            # Normalize so top-left-most block is (0, 0)
            curr_sorted = sorted(curr)
            base_r, base_c = curr_sorted[0]
            normalized = tuple(sorted((r - base_r, c - base_c) for r, c in curr_sorted))
            variations.add(normalized)
        # Flip (r, c) -> (r, -c)
        curr = [(r, -c) for r, c in curr]
    return variations


def findFirstEmptyCell(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 0:
                return r, c
    return None, None


def solve(shape_counts, grid, all_variants, shape_areas, remaining_area, empty_cells):
    # All shapes placed
    if remaining_area == 0:
        return True

    # Not enough space left in grid to fit remaining shapes
    if empty_cells < remaining_area:
        return False

    r, c = findFirstEmptyCell(grid)
    if r is None:
        return remaining_area == 0

    # Try to place a shape at the current (r, c)
    for shape_id, count in shape_counts.items():
        if count > 0:
            for variant in all_variants[shape_id]:
                fit = True
                for dr, dc in variant:
                    nr, nc = r + dr, c + dc
                    if not (
                        0 <= nr < len(grid)
                        and 0 <= nc < len(grid[0])
                        and grid[nr][nc] == 0
                    ):
                        fit = False
                        break

                if fit:
                    # Place
                    for dr, dc in variant:
                        grid[r + dr][c + dc] = 1
                    shape_counts[shape_id] -= 1

                    if solve(
                        shape_counts,
                        grid,
                        all_variants,
                        shape_areas,
                        remaining_area - shape_areas[shape_id],
                        empty_cells - shape_areas[shape_id],
                    ):
                        return True

                    # Backtrack
                    shape_counts[shape_id] += 1
                    for dr, dc in variant:
                        grid[r + dr][c + dc] = 0

    # Skip this cell only if we have enough empty cells left
    if empty_cells > remaining_area:
        grid[r][c] = -1
        if solve(
            shape_counts,
            grid,
            all_variants,
            shape_areas,
            remaining_area,
            empty_cells - 1,
        ):
            return True

        # Backtrack
        grid[r][c] = 0

    return False


if __name__ == "__main__":
    shapes, checks = readInput("./input.txt")

    # Find the variants and the shapes for each shape
    all_variants = {sid: getAllVariations(coords) for sid, coords in shapes.items()}
    shape_areas = {sid: len(coords) for sid, coords in shapes.items()}

    res = 0
    for (w, h), values in checks:
        grid = [[0] * w for _ in range(h)]
        shape_counts = {i: count for i, count in enumerate(values) if count > 0}
        total_area = sum(shape_areas[i] * count for i, count in shape_counts.items())

        if total_area <= (w * h):
            if solve(shape_counts, grid, all_variants, shape_areas, total_area, w * h):
                res += 1

    print(f"Result: {res}")
