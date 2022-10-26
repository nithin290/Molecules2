class Player:

    def __init__(self, id=0, color=None, name=""):
        if color is None:
            color = [0, 0, 0]
        self.id = id

        self.color = color
        self.name = name
        self.next_player = -1
        self.prev_player = -1

    def __repr__(self):
        return f'{self.id}:{self.next_player}:{self.prev_player}'
        # return self.name
