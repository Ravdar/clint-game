class GameStats:
    def __init__(self, clint_game):

        self.reset_stats()
        self.game_over = False
        self.game_active = False

    def reset_stats(self):
        self.score = 0
        self.lifes_left = 3
