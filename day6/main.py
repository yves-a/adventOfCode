def readInput(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    matrix = []
    operations = []
    for line in lines:
        line = line.strip("\n")
        if all(c in "0123456789 " for c in line):
            # Changed for Part 2, just append the entire line
            matrix.append(line)
        elif all(c in "*+ " for c in line):
            ops = line.split()
            operations.append(ops)
    return matrix, operations


def applyOperations(matrix, operations):
    # Calculate in columns
    # Part 1
    totalSum = 0
    for j in range(len(matrix[0])):
        currTotal = 0 if operations[j] == "+" else 1
        for i in range(len(matrix)):
            if operations[j] == "+":
                currTotal += matrix[i][j]
            else:
                currTotal *= matrix[i][j]
        totalSum += currTotal

    return totalSum


def applyOperationsRightToLeft(matrix, operations):
    # Part 2
    operation_index = 0
    total = 0
    currTotal = 0 if operations[operation_index] == "+" else 1
    for j in range(len(matrix[0])):
        currDigit = ""
        for i in range(len(matrix)):
            currDigit += matrix[i][j] if matrix[i][j] != " " else ""

        if currDigit == "":
            total += currTotal
            operation_index += 1
            currTotal = 0 if operations[operation_index] == "+" else 1
            continue

        if operations[operation_index] == "+":
            currTotal += int(currDigit)
        else:
            currTotal *= int(currDigit)

    total += currTotal

    return total


if __name__ == "__main__":
    matrix, operations = readInput("./input.txt")

    # Part 1
    # print(applyOperations(matrix, operations[0]))

    # Part 2
    print(applyOperationsRightToLeft(matrix, operations[0]))
