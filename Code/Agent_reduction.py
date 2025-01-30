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
        entry_input = input().replace(',', ',').split(',')
        if len(entry_input) == 2:
            entryPoint = tuple(map(int, entry_input))
            if (entryPoint[0] < 0 or entryPoint[0] >= rows or
                    entryPoint[1] < 0 or entryPoint[1] >= cols or
                    matrixA[entryPoint[0]][entryPoint[1]] not in (-1, 1)):
                print("Invalid entry point:", entryPoint)
                print("value: ", matrixA[entryPoint[0]][entryPoint[1]])
            else:
                print("Valid entry point:", entryPoint)
                entry_valid = True
        else:
            print("Invalid input. Please enter the path entry point as 'row,col'.")

    exit_valid = False
    while not exit_valid:
        print("Enter the path exit point (row, col):")
        exit_input = input().replace(',', ',').split(',')
        if len(exit_input) == 2:
            exitPoint = tuple(map(int, exit_input))
            if (exitPoint[0] < 0 or exitPoint[0] >= rows or
                    exitPoint[1] < 0 or exitPoint[1] >= cols or
                    matrixA[exitPoint[0]][exitPoint[1]] not in (-1, 1)):
                print("Invalid exit point:", exitPoint)
                print("value: ", matrixA[exitPoint[0]][exitPoint[1]])
            else:
                print("Valid exit point:", exitPoint)
                exit_valid = True
        else:
            print("Invalid input. Please enter the path exit point as 'row,col'.")

    return matrixA, entryPoint, exitPoint

def print_matrix(matrixA):
    for row in matrixA:
        print(" ".join(map(str, row)))

def search_path(matrixA, currentPoint, pathflag, last_agent_point, pathindex, previousCrossIndex):
    """
    Searches for the next path point in either row (r) or column (c), or both (i).
    Returns:
      nextPoint, newPathFlag, add_agent, pathindex, previousCrossIndex
    """
    print(f"Searching from {currentPoint} in direction {pathflag}")
    rows = len(matrixA)
    cols = len(matrixA[0])
    row0, col0 = currentPoint

    add_agent = 0
    nextPoint = None

    def walk_cells(cells, pathindex, previousCrossIndex):
        nonlocal add_agent
        print("previousCrossIndex:", previousCrossIndex)
        for (r, c) in cells:
            # If it's a blank path cell, mark it with the current pathindex
            if matrixA[r][c] == 0:
                matrixA[r][c] = pathindex

            # If we detect a "zigzag" or crossing
            elif matrixA[r][c] == previousCrossIndex:
                print(f"Zigzag detected at {(r, c)}")
                add_agent = 0

            elif (matrixA[r][c] not in (0, 1, -1)
                  and matrixA[r][c] != previousCrossIndex):
                # Found a crossing to another path
                add_agent = 1
                previousCrossIndex = matrixA[r][c]
                print(f"Crossing {previousCrossIndex} at {(r, c)}. Updating previousCrossIndex to {previousCrossIndex}")

        return pathindex, add_agent, previousCrossIndex

    # Based on the direction flag, search row-wise or column-wise
    if pathflag == 'r':
        for col in range(cols):
            if col != col0 and matrixA[row0][col] in (1, -1):
                nextPoint = (row0, col)
                step = 1 if col > col0 else -1
                path_cells = [(row0, c) for c in range(col0, col + step, step)]
                pathindex, add_agent, previousCrossIndex = walk_cells(path_cells, pathindex, previousCrossIndex)
                return nextPoint, 'c', add_agent, pathindex, previousCrossIndex
        return None, 'r', add_agent, pathindex, previousCrossIndex

    elif pathflag == 'c':
        for row in range(rows):
            if row != row0 and matrixA[row][col0] in (1, -1):
                nextPoint = (row, col0)
                step = 1 if row > row0 else -1
                path_cells = [(r, col0) for r in range(row0, row + step, step)]
                pathindex, add_agent, previousCrossIndex = walk_cells(path_cells, pathindex, previousCrossIndex)
                return nextPoint, 'r', add_agent, pathindex, previousCrossIndex
        return None, 'c', add_agent, pathindex, previousCrossIndex

    else:
        # Initial direction "i" => Try row first, then column
        # 1) Try moving horizontally first
        for col in range(cols):
            if col != col0 and matrixA[row0][col] in (1, -1):
                nextPoint = (row0, col)
                step = 1 if col > col0 else -1
                path_cells = [(row0, c) for c in range(col0, col + step, step)]
                pathindex, add_agent, previousCrossIndex = walk_cells(path_cells, pathindex, previousCrossIndex)
                return nextPoint, 'c', add_agent, pathindex, previousCrossIndex

        # 2) Then try moving vertically
        for row in range(rows):
            if row != row0 and matrixA[row][col0] in (1, -1):
                nextPoint = (row, col0)
                step = 1 if row > row0 else -1
                path_cells = [(r, col0) for r in range(row0, row + step, step)]
                pathindex, add_agent, previousCrossIndex = walk_cells(path_cells, pathindex, previousCrossIndex)
                return nextPoint, 'r', add_agent, pathindex, previousCrossIndex

        # If no path found, return None
        return None, 'i', add_agent, pathindex, previousCrossIndex

def compute_agent_reduction(matrix, entry, exit_):
    print("\nRunning Agent Reduction Algorithm...")

    pathflag = "i"
    currentPoint = exit_
    # Start your linked list with the exit point labeled as "agent"
    head = Node(currentPoint, "agent")
    currentNode = head

    # We'll store all visited points in a list for the GUI
    path_list = []
    path_list.append(exit_)

    pathindex = 2
    previousCrossIndex = -2

    while currentPoint != entry:
        print(f"\nCurrentPoint: {currentPoint}, pathflag: {pathflag}, pathindex: {pathindex}")
        nextPoint, pathflag, add_agent, pathindex, previousCrossIndex = search_path(
            matrix, currentPoint, pathflag,
            last_agent_point=None,  # or keep track if needed
            pathindex=pathindex,
            previousCrossIndex=previousCrossIndex
        )

        if not nextPoint:
            print("No more path found; stopping.")
            break

        # If we detect an agent crossing, increment pathindex
        if add_agent == 1:
            print(f"Crossing detected -> incrementing pathindex from {pathindex} to {pathindex + 1}")
            currentNode.point_identifier = "agent"
            pathindex += 1

        # Decide how to label the node
        if nextPoint == entry or add_agent == 1:
            newNode = Node(nextPoint, "agent")
        else:
            newNode = Node(nextPoint, "path")

        currentNode.next = newNode
        currentNode = newNode
        currentPoint = nextPoint

        # Add to path_list
        path_list.append(nextPoint)

    # Return BOTH the path_list (for the GUI) and the head of the linked list
    return path_list, head

if __name__ == "__main__":
    matrixA, entryPoint, exitPoint = read_path()
    print("\nInitial matrix:")
    print_matrix(matrixA)
    print(f"\nEntry point: {entryPoint} (Agent)")
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

    # For debugging, show the collected path list
    print("\nPath List (from exit -> entry):")
    print(path)