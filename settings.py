class Settings:
    def __init__(self):
        self.bg_color = (246, 148, 37)
        self.ground_color = (126, 65, 36)
        self.grass_color = (46, 77, 15)
        self.clint_speed = 12
        self.bullet_width = 35
        self.bullet_height = 35
        self.bullet_speed = 10
        self.belfer_speed = 1
        self.speed_increase = 0.004
        self.clint_gravity = 2
        self.goat_gravity = 2
        self.spawn_pause_decrease = 0.15
        self.intouchable_time = 2500

        self.starting_settings()

    def starting_settings(self):
        self.game_speed = 4
        self.spawn_pause = 2500  # 3000
