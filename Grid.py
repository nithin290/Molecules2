from Cell import Cell
from Cell import CellType


class Grid:

    def __init__(self, rows, cols):
        self.matrix = [[Cell() for _ in range(cols)] for __ in range(rows)]
        self.rows = rows
        self.cols = cols

        # setting vibration factor and cell type at grid vertices
        self.matrix[0][0].vibrate_factor = self.matrix[rows - 1][0].vibrate_factor = \
            self.matrix[0][cols - 1].vibrate_factor = self.matrix[rows - 1][cols - 1].vibrate_factor = 0.75
        self.matrix[0][cols - 1].set_type(CellType.VERTEX)

        # setting vibration factor at grid edges
        for i in range(1, rows - 1):
            self.matrix[i][0].vibrate_factor = 0.5
            self.matrix[i][cols - 1].vibrate_factor = 0.5
            self.matrix[i][0].set_type(CellType.SIDE)
            self.matrix[i][cols - 1].set_type(CellType.SIDE)
        for i in range(1, cols - 1):
            self.matrix[0][i].vibrate_factor = 0.5
            self.matrix[0][i].set_type(CellType.INTERNAL)
            self.matrix[rows - 1][i].vibrate_factor = 0.5
            self.matrix[rows - 1][i].set_type(CellType.INTERNAL)

        # adding neighbors to each of the cells
        for i in range(self.rows):
            for j in range(self.cols):
                if i > 0:
                    self.matrix[i][j].neighbors.append(self.matrix[i - 1][j])
                if i < self.rows - 1:
                    self.matrix[i][j].neighbors.append(self.matrix[i + 1][j])
                if j < self.cols - 1:
                    self.matrix[i][j].neighbors.append(self.matrix[i][j + 1])
                if j > 0:
                    self.matrix[i][j].neighbors.append(self.matrix[i][j - 1])

    def print_grid(self):
        for i in range(self.rows):
            print(i)
            for j in range(self.cols):
                print(j)
                print(self.matrix[i][j].noAtoms, end=" ")
            print()
        print()
