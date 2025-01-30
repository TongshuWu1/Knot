import tkinter as tk
from tkinter import messagebox
import Agent_reduction
from pathNode import Node

class AgentReductionGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x700")
        self.root.title("Agent Reduction - Path Optimization")

        # Title
        self.label_title = tk.Label(root, text="Agent Reduction", font=("Arial", 18), fg="black", bg="lightgray")
        self.label_title.pack(pady=10, fill=tk.X)

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

        # Output Labels
        self.path_label = tk.Label(root, text="Path: ")
        self.path_label.pack()
        self.original_points_label = tk.Label(root, text="Total number of original points: ")
        self.original_points_label.pack()
        self.agents_needed_label = tk.Label(root, text="Total number of agents needed after reduction: ")
        self.agents_needed_label.pack()

    def run_algorithm(self):
        try:
            # Read matrix input
            matrix_str = self.matrix_text.get("1.0", tk.END).strip()
            matrix_lines = matrix_str.split("\n")
            matrix = [list(map(int, line.split(','))) for line in matrix_lines]

            rows = len(matrix)
            cols = len(matrix[0])

            if rows != cols:
                messagebox.showerror("Error", "Matrix must be square (rows must equal columns)")
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

            # Check if entry and exit points are valid (either 1 or -1)
            if matrix[entry[0]][entry[1]] not in (1, -1):
                messagebox.showerror("Error", "Entry point must be either 1 or -1")
                return
            if matrix[exit_[0]][exit_[1]] not in (1, -1):
                messagebox.showerror("Error", "Exit point must be either 1 or -1")
                return

            # Run the actual agent reduction algorithm
            path, head = Agent_reduction.compute_agent_reduction(matrix, entry, exit_)

            # Convert path to list of tuples (row, col, type)
            path_list = []
            current_node = head
            while current_node:
                path_list.append((current_node.data[0], current_node.data[1], current_node.point_identifier))
                current_node = current_node.next

            # Draw Path
            self.draw_grid(matrix, path_list)

            # Output the path in a list and the total number of original points and agents needed after reduction
            original_points = len(path_list)
            agents_needed = sum(1 for point in path_list if point[2] == "agent")
            self.path_label.config(text=f"Path: {path_list}")
            self.original_points_label.config(text=f"Total number of original points: {original_points}")
            self.agents_needed_label.config(text=f"Total number of agents needed after reduction: {agents_needed}")

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def draw_grid(self, matrix, path):
        """
        Draw the matrix with the path on the canvas
        """
        self.canvas.delete("all")  # Clear previous drawings
        rows, cols = len(matrix), len(matrix[0])
        cell_size = min(400 // rows, 400 // cols)  # Adjust grid size

        # Draw the grid
        for r in range(rows):
            for c in range(cols):
                x1, y1 = c * cell_size, r * cell_size
                x2, y2 = (c + 1) * cell_size, (r + 1) * cell_size

                fill_color = "white"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="gray")

        # Draw the path
        for i in range(len(path) - 1):
            x1, y1 = path[i][1] * cell_size + cell_size // 2, path[i][0] * cell_size + cell_size // 2
            x2, y2 = path[i + 1][1] * cell_size + cell_size // 2, path[i + 1][0] * cell_size + cell_size // 2

            # Draw red line between nodes with arrow pointing in the opposite direction
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2, arrow=tk.FIRST)

            # Draw blue dot if an agent is needed
            if path[i][2] == "agent":
                self.canvas.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3, fill="blue")

        # Draw blue dot for the last node if it is an agent
        if path[-1][2] == "agent":
            x1, y1 = path[-1][1] * cell_size + cell_size // 2, path[-1][0] * cell_size + cell_size // 2
            self.canvas.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3, fill="blue")

# Run GUI
root = tk.Tk()
app = AgentReductionGUI(root)
root.mainloop()