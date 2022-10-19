# Class for Each Spot in Grid
class Cell:

    def __init__(self):
        self.color = [0, 0, 0]
        self.neighbors = []
        self.noAtoms = 0
        self.vibrate_factor = 0.25   # default vibration factor for most of the internal cells

    # def __repr__(self):
    #     return f'{self.noAtoms}'
