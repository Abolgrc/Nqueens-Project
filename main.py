import tkinter as tk
from tkinter import messagebox
from solvers import BacktrackingSolver, GeneticSolver, CSPSolver

class NQueensGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("N-Queens Solver")
        self.window.geometry("450x600")
        
        tk.Label(self.window, text="Enter N:").pack(pady=5)
        self.n_entry = tk.Entry(self.window)
        self.n_entry.pack()
        
        self.algorithm_var = tk.StringVar(value="backtracking")
        tk.Label(self.window, text="Select Algorithm:").pack(pady=5)
        tk.Radiobutton(self.window, text="Backtracking", variable=self.algorithm_var, value="backtracking").pack()
        tk.Radiobutton(self.window, text="Genetic Algorithm", variable=self.algorithm_var, value="genetic").pack()
        tk.Radiobutton(self.window, text="CSP", variable=self.algorithm_var, value="csp").pack()
        
        tk.Button(self.window, text="Solve", command=self.solve).pack(pady=10)
        
        self.canvas = tk.Canvas(self.window, width=400, height=400, bg="white")
        self.canvas.pack(pady=10)
        
        self.window.mainloop()
    
    def solve(self):
        try:
            n = int(self.n_entry.get())
            if n < 1:
                messagebox.showerror("Error", "N must be a positive integer")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for N")
            return
        
        if n == 1:
            solution = [0]
            self.display_solution(solution)
            return
        elif n == 2 or n == 3:
            messagebox.showinfo("No Solution", f"No solution exists for N={n}")
            return
        
        algorithm = self.algorithm_var.get()
        if algorithm == "backtracking":
            solver = BacktrackingSolver()
        elif algorithm == "genetic":
            solver = GeneticSolver()
        elif algorithm == "csp":
            solver = CSPSolver()
        else:
            messagebox.showerror("Error", "Unknown algorithm selected")
            return

        solution = solver.solve(n)
        
        if solution:
            self.display_solution(solution)
        else:
            messagebox.showinfo("Result", "No solution found within constraints")
    
    def display_solution(self, solution):
        self.canvas.delete("all")
        n = len(solution)
        square_size = 400 / n
        
        for i in range(n):
            for j in range(n):
                x0, y0 = j * square_size, i * square_size
                x1, y1 = (j + 1) * square_size, (i + 1) * square_size
                color = "white" if (i + j) % 2 == 0 else "white"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
                if solution[j] == i:
                    self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text="Q", font=("Arial", int(square_size / 2)))

if __name__ == "__main__":
    NQueensGUI()
