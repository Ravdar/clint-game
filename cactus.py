import pygame
from pygame.sprite import Sprite
import random


class Cactus(Sprite):
    def __init__(self, clint_game):
        super().__init__()
        self.screen = clint_game.screen
        self.settings = clint_game.settings
        self.screen_rect = self.screen.get_rect()
        self.screen_width = clint_game.screen_width
        self.screen_height = clint_game.screen_height

        self.cactus_sizes = [
            num
            for num in range(
                int(0.071 * self.screen_height), int(0.114 * self.screen_height)
            )
        ]
        self.cactus_types = [num for num in range(1, 4)]

        self.size = random.choice(self.cactus_sizes)
        self.cactus_type = random.choice(self.cactus_types)

        if self.cactus_type == 1:
            self.original_image = pygame.image.load("images/enemies/cacti/cactus.png")
        elif self.cactus_type == 2:
            self.original_image = pygame.image.load("images/enemies/cacti/cactus2.png")
        else:
            self.original_image = pygame.image.load("images/enemies/cacti/cactus3.png")

        self.image = pygame.transform.scale(
            self.original_image, (self.size, self.size)
        ).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = 0.845 * self.screen_height
        self.rect.left = self.screen_width

        self.x = float(self.rect.x)

    def update(self):
        self.x -= self.settings.game_speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)
