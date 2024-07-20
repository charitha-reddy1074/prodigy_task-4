import tkinter as tk
from tkinter import messagebox
import random

class SudokuSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        
        # Configure background color
        self.root.configure(bg="#363636")  # Dark grey background
        
        # Define colors for numbers
        self.number_colors = ['#ff1aff', '#00ff00', '#ffff00', '#00ffff', '#ff00ff']  # Neon colors
        
        # Create 9x9 grid of Entry widgets and frames for 3x3 blocks
        self.entry_grid = [[None]*9 for _ in range(9)]
        self.frames = [[tk.Frame(root, bg="#363636") for _ in range(3)] for _ in range(3)]
        
        for i in range(9):
            for j in range(9):
                color = random.choice(self.number_colors)
                frame_row = i // 3
                frame_col = j // 3
                self.entry_grid[i][j] = tk.Entry(self.frames[frame_row][frame_col], width=2, font=("Arial", 20), bg="#595959", fg="white", highlightbackground=color, highlightcolor=color, highlightthickness=2)
                self.entry_grid[i][j].grid(row=i % 3, column=j % 3, padx=2, pady=2)
                self.frames[frame_row][frame_col].grid(row=frame_row, column=frame_col, padx=2, pady=2)
        
        # Solve button
        self.solve_button = tk.Button(root, text="Solve Sudoku", command=self.solve_sudoku, bg="#ff1aff", fg="#363636", font=("Arial", 12, "bold"))
        self.solve_button.grid(row=9, column=4, pady=10)
        
        # Result label for status messages
        self.result_label = tk.Label(root, text="", bg="#363636", fg="#ff1aff", font=("Arial", 14, "bold"))
        self.result_label.grid(row=10, columnspan=9, pady=10)
    
    def solve_sudoku(self):
        grid = [[0]*9 for _ in range(9)]
        
        # Retrieve values from entry widgets
        for i in range(9):
            for j in range(9):
                value = self.entry_grid[i][j].get()
                if value.isdigit() and 1 <= int(value) <= 9:
                    grid[i][j] = int(value)
                else:
                    grid[i][j] = 0
        
        # Solve Sudoku using backtracking algorithm (recursive)
        if self.solve(grid):
            # Update GUI with solved values
            for i in range(9):
                for j in range(9):
                    self.entry_grid[i][j].delete(0, tk.END)
                    self.entry_grid[i][j].insert(0, grid[i][j])
                    if grid[i][j] != 0:
                        color = random.choice(self.number_colors)
                        self.entry_grid[i][j].configure(fg=color)
            self.result_label.config(text="Sudoku solved successfully!", fg="#ff1aff")
        else:
            self.result_label.config(text="No solution exists for this Sudoku.", fg="#ff1aff")
    
    def solve(self, grid):
        # Find empty cell in Sudoku grid
        find = self.find_empty_cell(grid)
        if not find:
            return True  # Sudoku solved
        
        row, col = find
        
        for num in range(1, 10):
            if self.is_valid_move(grid, row, col, num):
                grid[row][col] = num
                
                if self.solve(grid):
                    return True
                
                grid[row][col] = 0  # Backtrack
        
        return False
    
    def is_valid_move(self, grid, row, col, num):
        # Check if num can be placed in grid[row][col]
        # Check row
        for i in range(9):
            if grid[row][i] == num:
                return False
        
        # Check column
        for i in range(9):
            if grid[i][col] == num:
                return False
        
        # Check 3x3 subgrid
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[start_row + i][start_col + j] == num:
                    return False
        
        return True
    
    def find_empty_cell(self, grid):
        # Find first empty cell in grid
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverApp(root)
    root.mainloop()
