import tkinter as tk
from tkinter import messagebox
import Agent_reduction
from pathNode import Node

class AgentReductionGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x600")
        self.root.title("Agent Reduction - Path Optimization")

        # Title
        self.label_title = tk.Label(root, text="Agent Reduction", font=("Arial", 18), fg="black", bg="lightgray")
        self.label_title.pack(pady=10, fill=tk.X)

        # Matrix size inputs
        self.size_frame = tk.Frame(root)
        self.size_frame.pack(pady=5)
        tk.Label(self.size_frame, text="Rows:").pack(side=tk.LEFT)
        self.rows_entry = tk.Entry(self.size_frame, width=5)
        self.rows_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.size_frame, text="Cols:").pack(side=tk.LEFT)
        self.cols_entry = tk.Entry(self.size_frame, width=5)
        self.cols_entry.pack(side=tk.LEFT, padx=5)

        # Matrix Input Text Area
        self.matrix_label = tk.Label(root, text="Enter Matrix (comma separated):")
        self.matrix_label.pack()

        self.matrix_text = tk.Text(root, height=8, width=50)
        self.matrix_text.pack()

        # Entry and Exit Point Inputs
        self.entry_exit_frame = tk.Frame(root)
        self.entry_exit_frame.pack(pady=5)

        tk.Label(self.entry_exit_frame, text="Entry (row, col):").pack(side=tk.LEFT)
        self.entry_point = tk.Entry(self.entry_exit_frame, width=10)
        self.entry_point.pack(side=tk.LEFT, padx=5)

        tk.Label(self.entry_exit_frame, text="Exit (row, col):").pack(side=tk.LEFT)
        self.exit_point = tk.Entry(self.entry_exit_frame, width=10)
        self.exit_point.pack(side=tk.LEFT, padx=5)

        # Run Button
        self.run_button = tk.Button(root, text="Run Agent Reduction", command=self.run_algorithm)
        self.run_button.pack(pady=10)

        # Canvas for Path Visualization
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack(pady=10)

    def run_algorithm(self):
        try:
            # Get matrix size
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())

            # Read matrix input
            matrix_str = self.matrix_text.get("1.0", tk.END).strip()
            matrix_lines = matrix_str.split("\n")
            matrix = [list(map(int, line.split(','))) for line in matrix_lines]

            if len(matrix) != rows or any(len(row) != cols for row in matrix):
                messagebox.showerror("Error", "Matrix size does not match input dimensions")
                return

            # Read entry and exit points
            entry = tuple(map(int, self.entry_point.get().split(',')))
            exit_ = tuple(map(int, self.exit_point.get().split(',')))

            if not (0 <= entry[0] < rows and 0 <= entry[1] < cols):
                messagebox.showerror("Error", "Invalid Entry Point")
                return
            if not (0 <= exit_[0] < rows and 0 <= exit_[1] < cols):
                messagebox.showerror("Error", "Invalid Exit Point")
                return

            # Run the actual agent reduction algorithm
            path = self.compute_agent_reduction(matrix, entry, exit_)

            # Draw Path
            self.draw_grid(matrix, path)

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def compute_agent_reduction(self, matrix, entry, exit_):
        """
        Uses the Agent_reduction.py logic to compute the path.
        """
        print("\nRunning Agent Reduction Algorithm...")

        # Initialize variables
        pathflag = "i"  # Initial direction
        currentPoint = exit_
        head = Node(currentPoint, "agent")  # Exit point is always an agent
        currentNode = head
        visited_points = set()
        visited_points.add(exit_)

        path = {exit_, entry}  # Include entry & exit in the path

        while currentPoint != entry:
            # Fix: Correctly call search_path
            nextPoint, pathflag, add_agent = Agent_reduction.search_path(matrix, currentPoint, pathflag)

            if not nextPoint:
                print("No more path found; stopping.")
                break

            # Store the path
            path.add(nextPoint)

            # Mark entry point as an agent
            if nextPoint == entry:
                newNode = Node(nextPoint, "agent")
            else:
                newNode = Node(nextPoint, "agent" if add_agent == 1 else "path")

            currentNode.next = newNode
            currentNode = newNode
            currentPoint = nextPoint
            visited_points.add(nextPoint)

        return path  # Return path as a set
    def draw_grid(self, matrix, path):
        """
        Draw the matrix with the path on the canvas
        """
        self.canvas.delete("all")  # Clear previous drawings
        rows, cols = len(matrix), len(matrix[0])
        cell_size = min(100 // rows, 100 // cols)  # Adjust grid size

        for r in range(rows):
            for c in range(cols):
                x1, y1 = c * cell_size, r * cell_size
                x2, y2 = (c + 1) * cell_size, (r + 1) * cell_size

                fill_color = "white"
                if matrix[r][c] == -1:
                    fill_color = "black"  # Walls
                elif (r, c) in path:
                    fill_color = "red"  # Agent Path
                elif matrix[r][c] == 2:
                    fill_color = "blue"  # Reduced Agent Spot

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="gray")

# Run GUI
root = tk.Tk()
app = AgentReductionGUI(root)
root.mainloop()