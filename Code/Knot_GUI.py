import tkinter as tk
from tkinter import messagebox
import Agent_reduction  # Make sure this has your updated code
from pathNode import Node


class AgentReductionGUI:
    def __init__(self, root):
        self.root = root
        # Set initial window size (you can remove or adjust as needed)
        self.root.geometry("600x700")
        self.root.title("Agent Reduction - Path Optimization")

        # ============ 1) Main Scrollable Frame Setup ============
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for scrolling
        self.my_canvas = tk.Canvas(main_frame)
        self.my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        self.my_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.my_canvas.yview)
        self.my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas
        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        self.my_canvas.bind(
            "<Configure>",
            lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))
        )

        # Frame inside the canvas (this is our "scrollable" frame)
        self.second_frame = tk.Frame(self.my_canvas)
        self.my_canvas.create_window((0, 0), window=self.second_frame, anchor="nw")

        # ============ 2) Place Your Widgets inside second_frame ============

        # Title
        self.label_title = tk.Label(
            self.second_frame, text="Agent Reduction",
            font=("Arial", 18), fg="black", bg="lightgray"
        )
        self.label_title.pack(pady=10, fill=tk.X)

        # Matrix Input Text Area
        self.matrix_label = tk.Label(self.second_frame, text="Enter Matrix (comma separated):")
        self.matrix_label.pack()

        self.matrix_text = tk.Text(self.second_frame, height=8, width=50)
        self.matrix_text.pack()

        # Frame for Entry and Exit Points
        self.entry_exit_frame = tk.Frame(self.second_frame)
        self.entry_exit_frame.pack(pady=5)

        tk.Label(self.entry_exit_frame, text="Entry (row, col):").pack(side=tk.LEFT)
        self.entry_point = tk.Entry(self.entry_exit_frame, width=10)
        self.entry_point.pack(side=tk.LEFT, padx=5)

        tk.Label(self.entry_exit_frame, text="Exit (row, col):").pack(side=tk.LEFT)
        self.exit_point = tk.Entry(self.entry_exit_frame, width=10)
        self.exit_point.pack(side=tk.LEFT, padx=5)

        # Run Button
        self.run_button = tk.Button(self.second_frame, text="Run Agent Reduction", command=self.run_algorithm)
        self.run_button.pack(pady=10)

        # Canvas for Path Visualization
        self.canvas = tk.Canvas(self.second_frame, width=400, height=400, bg="white")
        self.canvas.pack(pady=10)

        # Path Output
        self.path_title_label = tk.Label(self.second_frame, text="Path from Entry to Exit:")
        self.path_title_label.pack()

        self.path_frame = tk.Frame(self.second_frame)
        self.path_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        self.path_scrollbar = tk.Scrollbar(self.path_frame)
        self.path_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.path_text = tk.Text(self.path_frame, height=8, width=50, yscrollcommand=self.path_scrollbar.set)
        self.path_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.path_scrollbar.config(command=self.path_text.yview)

        # Labels for summary info
        self.original_points_label = tk.Label(self.second_frame, text="Total number of original points: ")
        self.original_points_label.pack()

        self.agents_needed_label = tk.Label(self.second_frame, text="Total number of agents needed after reduction: ")
        self.agents_needed_label.pack()

    def run_algorithm(self):
        """
        Reads the matrix, entry, and exit from GUI.
        Runs the agent reduction algorithm from Agent_reduction.
        Shows the results in the path_text widget and draws the path on self.canvas.
        """
        try:
            # Read matrix input
            matrix_str = self.matrix_text.get("1.0", tk.END).strip()
            matrix_lines = matrix_str.split("\n")
            matrix = [list(map(int, line.split(','))) for line in matrix_lines if line.strip()]

            rows = len(matrix)
            cols = len(matrix[0]) if rows > 0 else 0

            # Optional: Check if the matrix must be square
            # (Remove if you don't need a strict square matrix)
            if rows != cols:
                messagebox.showerror("Error", "Matrix must be square (rows must equal columns)")
                return

            # Read entry and exit points
            entry = tuple(map(int, self.entry_point.get().split(',')))
            exit_ = tuple(map(int, self.exit_point.get().split(',')))

            # Validate coordinates
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

            # Run the actual (updated) agent reduction algorithm
            path, head = Agent_reduction.compute_agent_reduction(matrix, entry, exit_)

            # Convert linked list to a list of (row, col, 'agent' or 'path')
            path_list = []
            current_node = head
            while current_node:
                r, c = current_node.data
                pt_type = current_node.point_identifier
                path_list.append((r, c, pt_type))
                current_node = current_node.next

            # Reverse path_list if you want it from entry -> exit
            # (Currently, 'head' might start at exit; depends on your logic.)
            path_list.reverse()

            # Draw Path on the canvas
            self.draw_grid(matrix, path_list)

            # Show results
            self.path_text.delete("1.0", tk.END)
            self.path_text.insert(tk.END, f"{path_list}")

            original_points = len(path_list)
            agents_needed = sum(1 for point in path_list if point[2] == "agent")

            self.original_points_label.config(text=f"Total number of original points: {original_points}")
            self.agents_needed_label.config(text=f"Total number of agents needed after reduction: {agents_needed}")

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def draw_grid(self, matrix, path):
        """
        Draw the matrix with the path on the canvas.
        `path` is a list of (row, col, type).
        """
        self.canvas.delete("all")  # Clear previous drawings

        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0

        # Adjust cell size so that the entire matrix fits in 400x400
        cell_size = min(400 // max(rows, 1), 400 // max(cols, 1)) if rows and cols else 40

        # Draw the grid (with row,col labels in each cell)
        for r in range(rows):
            for c in range(cols):
                x1, y1 = c * cell_size, r * cell_size
                x2, y2 = (c + 1) * cell_size, (r + 1) * cell_size

                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")
                self.canvas.create_text(x1 + 5, y1 + 5, anchor=tk.NW,
                                        text=f"({r},{c})", font=("Arial", 8))

        # Draw the path lines (in red) + agent nodes (in blue)
        for i in range(len(path) - 1):
            (r1, c1, t1) = path[i]
            (r2, c2, t2) = path[i + 1]

            x1, y1 = c1 * cell_size + cell_size // 2, r1 * cell_size + cell_size // 2
            x2, y2 = c2 * cell_size + cell_size // 2, r2 * cell_size + cell_size // 2

            # Draw red line with an arrow
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2, arrow=tk.LAST)

            # If the current point is an agent, draw a blue dot
            if t1 == "agent":
                radius = 3
                self.canvas.create_oval(x1 - radius, y1 - radius, x1 + radius, y1 + radius, fill="blue")

        # Check the last point in the path
        if path and path[-1][2] == "agent":
            (rL, cL, _) = path[-1]
            xL, yL = cL * cell_size + cell_size // 2, rL * cell_size + cell_size // 2
            radius = 3
            self.canvas.create_oval(xL - radius, yL - radius, xL + radius, yL + radius, fill="blue")


# ============ Run GUI ============
if __name__ == "__main__":
    root = tk.Tk()
    app = AgentReductionGUI(root)
    root.mainloop()