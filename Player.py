class Player:
    player_count = 0

    def __init__(self, color=None, name=""):
        if color is None:
            color = [0, 0, 0]
        self.id = Player.player_count
        Player.player_count += 1

        self.color = color
        self.name = name
        self.next_player = -1
        self.prev_player = -1

    def __repr__(self):
        return f'{self.next_player}:{self.prev_player}'
        # return self.name
