# Class for Each Spot in Grid
class Cell:
    def __init__(self, border_color):
        self.color = border_color
        self.neighbors = []
        self.noAtoms = 0

    def addNeighbors(self, grid, rows, cols, i, j):
        if i > 0:
            self.neighbors.append(grid[i - 1][j])
        if i < rows - 1:
            self.neighbors.append(grid[i + 1][j])
        if j < cols - 1:
            self.neighbors.append(grid[i][j + 1])
        if j > 0:
            self.neighbors.append(grid[i][j - 1])
