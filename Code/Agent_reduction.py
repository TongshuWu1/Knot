from pathNode import Node

def read_path():
    global entryPoint, exitPoint
    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))

    matrixA = []

    # Read the matrix row by row
    print("Enter the matrix row by row (comma separated):")
    for i in range(rows):
        row = list(map(int, input().replace(',', ',').split(',')))
        matrixA.append(row)

    entry_valid = False
    while not entry_valid:
        print("Enter the path entry point (row, col):")
        entryPoint = tuple(map(int, input().replace(',', ',').split(',')))
        if (entryPoint[0] < 0 or entryPoint[0] >= rows or
                entryPoint[1] < 0 or entryPoint[1] >= cols or
                matrixA[entryPoint[0]][entryPoint[1]] not in (-1, 1)):
            print("Invalid entry point:", entryPoint)
        else:
            print("Valid entry point:", entryPoint)
            entry_valid = True

    exit_valid = False
    while not exit_valid:
        print("Enter the path exit point (row, col):")
        exitPoint = tuple(map(int, input().replace(',', ',').split(',')))
        if (exitPoint[0] < 0 or exitPoint[0] >= rows or
                exitPoint[1] < 0 or exitPoint[1] >= cols or
                matrixA[exitPoint[0]][exitPoint[1]] not in (-1, 1)):
            print("Invalid exit point:", exitPoint)
        else:
            print("Valid exit point:", exitPoint)
            exit_valid = True

    return matrixA, entryPoint, exitPoint


def print_matrix(matrixA):
    for row in matrixA:
        print(" ".join(map(str, row)))


def search_path(matrixA, currentPoint, pathflag):
    print(f"Searching from {currentPoint} in direction {pathflag}")
    rows = len(matrixA)
    cols = len(matrixA[0])
    row0, col0 = currentPoint

    add_agent = 0
    nextPoint = None

    def walk_cells(cells):
        nonlocal add_agent
        for (r, c) in cells:
            if matrixA[r][c] == 0:
                matrixA[r][c] = 2
            elif matrixA[r][c] == 2:
                add_agent = 1

    if pathflag == 'r':
        for col in range(cols):
            if col != col0 and matrixA[row0][col] in (1, -1):
                nextPoint = (row0, col)
                step = 1 if col > col0 else -1
                path_cells = [(row0, c) for c in range(col0, col + step, step)]
                walk_cells(path_cells)
                return nextPoint, 'c', add_agent
        return None, 'r', add_agent

    elif pathflag == 'c':
        for row in range(rows):
            if row != row0 and matrixA[row][col0] in (1, -1):
                nextPoint = (row, col0)
                step = 1 if row > row0 else -1
                path_cells = [(r, col0) for r in range(row0, row + step, step)]
                walk_cells(path_cells)
                return nextPoint, 'r', add_agent
        return None, 'c', add_agent

    else:
        for col in range(cols):
            if col != col0 and matrixA[row0][col] in (1, -1):
                nextPoint = (row0, col)
                step = 1 if col > col0 else -1
                path_cells = [(row0, c) for c in range(col0, col + step, step)]
                walk_cells(path_cells)
                return nextPoint, 'c', add_agent

        for row in range(rows):
            if row != row0 and matrixA[row][col0] in (1, -1):
                nextPoint = (row, col0)
                step = 1 if row > row0 else -1
                path_cells = [(r, col0) for r in range(row0, row + step, step)]
                walk_cells(path_cells)
                return nextPoint, 'r', add_agent

        return None, 'i', add_agent


if __name__ == "__main__":
    matrixA, entryPoint, exitPoint = read_path()
    print("The matrix is:")
    print_matrix(matrixA)
    print(f"Entry point: {entryPoint} (Agent)")
    print(f"Exit point: {exitPoint} (Agent)")

    # Initialize variables
    pathflag = "i"
    currentPoint = exitPoint
    head = Node(currentPoint, "agent")  # Exit point is always an agent
    currentNode = head

    visited_points = set()
    visited_points.add(exitPoint)

    while currentPoint != entryPoint:
        nextPoint, pathflag, add_agent = search_path(matrixA, currentPoint, pathflag)
        if not nextPoint:
            print("No more path found; stopping.")
            break

        # Mark entry point as an agent
        if nextPoint == entryPoint:
            newNode = Node(nextPoint, "agent")
        else:
            newNode = Node(nextPoint, "agent" if add_agent == 1 else "path")

        currentNode.next = newNode
        currentNode = newNode
        currentPoint = nextPoint
        visited_points.add(nextPoint)

    print("\nFinal matrix:")
    print_matrix(matrixA)

    print("\nLinked path:")
    node_ptr = head
    while node_ptr:
        node_ptr.print_node()
        node_ptr = node_ptr.next