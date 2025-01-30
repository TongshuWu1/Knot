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
            print("value: ", matrixA[entryPoint[0]][entryPoint[1]])
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
            print("value: ", matrixA[exitPoint[0]][exitPoint[1]])
        else:
            print("Valid exit point:", exitPoint)
            exit_valid = True

    return matrixA, entryPoint, exitPoint


def print_matrix(matrixA):
    for row in matrixA:
        print(" ".join(map(str, row)))
def search_path(matrixA, currentPoint, pathflag, last_agent_point):
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
                # Check if the previous 2 is in the same section
                if last_agent_point and (r, c) in last_agent_point:
                    print(f"Crossing previous section at: ({r}, {c})")
                    add_agent = 0
                else:
                    add_agent = 1

    if pathflag == 'r':
        for col in range(cols):
            if col != col0 and matrixA[row0][col] in (1, -1):
                nextPoint = (row0, col)
                step = 1 if col > col0 else -1
                path_cells = [(row0, c) for c in range(col0, col + step, step)]
                walk_cells(path_cells)
                print(f"Current section: row {row0}, columns {col0} to {col}")
                return nextPoint, 'c', add_agent
        return None, 'r', add_agent

    elif pathflag == 'c':
        for row in range(rows):
            if row != row0 and matrixA[row][col0] in (1, -1):
                nextPoint = (row, col0)
                step = 1 if row > row0 else -1
                path_cells = [(r, col0) for r in range(row0, row + step, step)]
                walk_cells(path_cells)
                print(f"Current section: column {col0}, rows {row0} to {row}")
                return nextPoint, 'r', add_agent
        return None, 'c', add_agent

    else:
        for col in range(cols):
            if col != col0 and matrixA[row0][col] in (1, -1):
                nextPoint = (row0, col)
                step = 1 if col > col0 else -1
                path_cells = [(row0, c) for c in range(col0, col + step, step)]
                walk_cells(path_cells)
                print(f"Current section: row {row0}, columns {col0} to {col}")
                return nextPoint, 'c', add_agent

        for row in range(rows):
            if row != row0 and matrixA[row][col0] in (1, -1):
                nextPoint = (row, col0)
                step = 1 if row > row0 else -1
                path_cells = [(r, col0) for r in range(row0, row + step, step)]
                walk_cells(path_cells)
                print(f"Current section: column {col0}, rows {row0} to {row}")
                return nextPoint, 'r', add_agent

        return None, 'i', add_agent

def compute_agent_reduction(matrix, entry, exit_):
    print("\nRunning Agent Reduction Algorithm...")

    pathflag = "i"
    currentPoint = exit_
    head = Node(currentPoint, "agent")
    currentNode = head
    visited_points = set()
    visited_points.add(exit_)

    path = {exit_, entry}
    last_agent_point = None

    while currentPoint != entry:
        nextPoint, pathflag, add_agent = search_path(matrix, currentPoint, pathflag, last_agent_point)

        if not nextPoint:
            print("No more path found; stopping.")
            break

        path.add(nextPoint)

        if add_agent == 1:
            currentNode.point_identifier = "agent"
            last_agent_point = nextPoint

        if nextPoint == entry or add_agent == 1:
            newNode = Node(nextPoint, "agent")
        else:
            newNode = Node(nextPoint, "path")

        currentNode.next = newNode
        currentNode = newNode
        currentPoint = nextPoint
        visited_points.add(nextPoint)

    return path, head

if __name__ == "__main__":
    matrixA, entryPoint, exitPoint = read_path()
    print("The matrix is:")
    print_matrix(matrixA)
    print(f"Entry point: {entryPoint} (Agent)")
    print(f"Exit point: {exitPoint} (Agent)")

    # Compute the agent reduction path
    path, head = compute_agent_reduction(matrixA, entryPoint, exitPoint)

    print("\nFinal matrix:")
    print_matrix(matrixA)

    print("\nLinked path:")
    node_ptr = head
    while node_ptr:
        node_ptr.print_node()
        node_ptr = node_ptr.next