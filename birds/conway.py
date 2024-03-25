import tkinter as tk
import random

# Set the size of the grid
GRID_SIZE = 25
CELL_SIZE = 20

class GameOfLife:
    def __init__(self, master):
        self.master = master
        self.master.title("Conway's Game of Life")
        self.canvas = tk.Canvas(self.master, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
        self.canvas.bind("<Button-1>", self.add_cell)  # Bind left mouse click to add_cell
        self.canvas.pack()
        self.grid = [[random.randint(0, 1) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.draw_grid()
        self.master.after(100, self.update)

    def count_neighbors(self, x, y):
        """Count the number of live neighbors around a given cell."""
        neighbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbors += self.grid[(x + i) % GRID_SIZE][(y + j) % GRID_SIZE]
        return neighbors

    def update_grid(self):
        """Update the grid based on the rules of the Game of Life."""
        new_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                neighbors = self.count_neighbors(x, y)
                if self.grid[x][y] == 1:
                    if neighbors == 2 or neighbors == 3:
                        new_grid[x][y] = 1
                else:
                    if neighbors == 3:
                        new_grid[x][y] = 1
        self.grid = new_grid

    def draw_grid(self):
        """Draw the grid on the canvas."""
        self.canvas.delete("all")
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if self.grid[x][y] == 1:
                    self.canvas.create_rectangle(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        (x + 1) * CELL_SIZE,
                        (y + 1) * CELL_SIZE,
                        fill="black",
                        outline="gray"
                    )

    def add_cell(self, event):
        """Add a new cell to the grid at the clicked location."""
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        self.grid[x][y] = 1
        self.draw_grid()

    def update(self):
        """Update the game state and redraw the grid."""
        self.update_grid()
        self.draw_grid()
        self.master.after(100, self.update)

# Create the main window and start the game
root = tk.Tk()
game = GameOfLife(root)
root.mainloop()