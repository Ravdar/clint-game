import pygame


class Horse:
    def __init__(self, clint_game):
        super().__init__()
        self.screen = clint_game.screen
        self.settings = clint_game.settings
        self.screen_rect = self.screen.get_rect()
        self.screen_width = clint_game.screen_width
        self.screen_height = clint_game.screen_height
        self.ground_level = clint_game.grass_y - 0.079 * self.screen_height

        self.original_image = pygame.image.load("images/others/horse/horse_walk1.png")
        self.image = pygame.transform.scale(
            self.original_image, (0.080 * self.screen_width, 0.11 * self.screen_height)
        )  # Tutaj zmienić tak, żeby wielkość była uzależniona od wielkości ekranu
        self.image = self.image.convert_alpha()
        self.image.set_colorkey((255, 255, 255))

        self.original_image2 = pygame.image.load("images/others/horse/horse_walk2.png")
        self.image2 = pygame.transform.scale(
            self.original_image2, (0.080 * self.screen_width, 0.11 * self.screen_height)
        )  # Tutaj zmienić tak, żeby wielkość była uzależniona od wielkości ekranu
        self.image2 = self.image2.convert_alpha()
        self.image2.set_colorkey((255, 255, 255))

        self.original_image3 = pygame.image.load("images/others/horse/horse_walk3.png")
        self.image3 = pygame.transform.scale(
            self.original_image3, (0.080 * self.screen_width, 0.11 * self.screen_height)
        )  # Tutaj zmienić tak, żeby wielkość była uzależniona od wielkości ekranu
        self.image3 = self.image3.convert_alpha()
        self.image3.set_colorkey((255, 255, 255))

        self.horse_walk = [self.image, self.image3, self.image2, self.image3]
        self.horse_index = 0
        self.walking_image = self.horse_walk[int(self.horse_index)]

        self.rect = self.image.get_rect()
        self.rect.right = self.screen_rect.left
        self.rect.top = 0.740 * self.screen_height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Caption part

        self.font = pygame.font.Font("fonts/ArcadeClassic.ttf", 28)
        self.horse_caption_image = self.font.render(
            "Your horse Stormy is running!  You  have  to  chase  him!",
            True,
            (255, 255, 255),
        )
        self.horse_caption_rect = self.horse_caption_image.get_rect()
        self.horse_caption_rect.centerx = self.screen_rect.centerx
        self.horse_caption_rect.bottom = 0.405 * self.screen_height

        # Gate part

        self.gate_original_image = pygame.image.load("images/others/gate.png")
        self.gate_image = pygame.transform.scale(self.gate_original_image, (300, 400))
        self.gate_image = self.gate_image.convert_alpha()
        self.gate_image.set_colorkey((255, 255, 255))

        self.gate_rect = self.gate_image.get_rect()
        self.gate_rect.bottom = 0.95 * self.screen_height
        self.gate_rect.left = self.screen_rect.right + 1.628 * self.screen_width

        self.xr = float(self.gate_rect.x)

    def update(self):
        self.x += self.settings.clint_speed + 1
        self.xr -= self.settings.game_speed
        self.rect.x = self.x
        self.gate_rect.x = self.xr

    def blitme(self):
        self.screen.blit(self.walking_image, self.rect)
        self.screen.blit(self.gate_image, self.gate_rect)
        if self.x < 1.302 * self.screen_width:
            self.screen.blit(self.horse_caption_image, self.horse_caption_rect)

    def animate_horse(self):

        if self.horse_index >= 4:
            self.horse_index = 0

        self.walking_image = self.horse_walk[int(self.horse_index)]

        self.horse_index += 0.1

