# Class for Each Spot in Grid


class CellType:
    VERTEX = 1
    SIDE = 2
    INTERNAL = 3


class Cell:

    def __init__(self):
        self.color = [0, 0, 0]
        self.neighbors = []
        self.noAtoms = 0
        self.vibrate_factor = 0.4  # default vibration factor for most of the internal cells
        self.type = CellType.INTERNAL

    # def __repr__(self):
    #     return f'{self.noAtoms}'

    def vibrate(self):
        v = self.vibrate_factor
        self.vibrate_factor *= -1
        return v

    def set_type(self, type):
        self.type = type

    def add_atoms(self):
        # if self.noAtoms <= self.type + 1:
        self.noAtoms += 1
