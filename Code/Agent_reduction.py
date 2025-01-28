def read_path():
    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))

    matrix = []

    # Read the matrix row by row
    print("Enter the matrix row by row (comma separated):")
    for i in range(rows):
        row = list(map(int, input().replace(',', ',').split(',')))
        matrix.append(row)

    entry_valid = False
    while not entry_valid:
        # Read entry point and validate it is a valid point
        print("Enter the path entry point (row, col):")
        entry = tuple(map(int, input().replace(',', ',').split(',')))
        if (entry[0] < 0 or entry[0] >= rows or
                entry[1] < 0 or entry[1] >= cols or
                matrix[entry[0]][entry[1]] not in (-1, 1)):
            print("Invalid entry point:", entry)
        else:
            print("Valid entry point:", entry)
            entry_valid = True

    exit_valid = False
    while not exit_valid:
        print("Enter the path exit point (row, col):")
        exit = tuple(map(int, input().replace(',', ',').split(',')))
        if (exit[0] < 0 or exit[0] >= rows or
                exit[1] < 0 or exit[1] >= cols or
                matrix[exit[0]][exit[1]] not in (-1, 1)):
            print("Invalid exit point:", exit)
        else:
            print("Valid exit point:", exit)
            exit_valid = True

    return matrix, entry, exit


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))


if __name__ == "__main__":
    matrix, entry, exit = read_path()
    print("The matrix is:")
    print_matrix(matrix)
    print(f"Entry point: {entry}")
    print(f"Exit point: {exit}")
