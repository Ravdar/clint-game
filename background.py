import pygame
from pygame.sprite import Sprite


class Background(Sprite):
    def __init__(self, clint_game, init_x):
        super().__init__()
        self.screen = clint_game.screen
        self.settings = clint_game.settings
        self.screen_rect = clint_game.screen_rect
        self.screen_height = clint_game.screen_height
        self.screen_width = clint_game.screen_width

        #  Sun
        self.sun_image = pygame.image.load("images/others/bg/sun.png")
        self.sun_image = pygame.transform.scale(
            self.sun_image, (100, 100)
        ).convert_alpha()
        self.sun_rect = self.sun_image.get_rect()
        self.sun_rect.x = 250
        self.sun_rect.y = self.screen_height * 1 / 21

        # Main background
        self.bg_image = pygame.image.load("images/others/bg/bg.png")
        self.bg_image = pygame.transform.scale(
            self.bg_image, (self.screen_width, self.screen_height * 7 / 8)
        )

        self.bg_rect = self.bg_image.get_rect()

        self.bg_rect.left = init_x

        self.x = float(self.bg_rect[0])

    def display_sun(self):
        self.screen.blit(self.sun_image, self.sun_rect)

    def update(self):
        self.x -= self.settings.game_speed / 3
        self.bg_rect.x = self.x

    def blit_bg(self):
        self.screen.blit(self.bg_image, self.bg_rect)
