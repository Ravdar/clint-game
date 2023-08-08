import pygame
from pygame.sprite import Sprite
import random


class Bomb(Sprite):
    def __init__(self, clint_game):
        super().__init__()
        self.screen = clint_game.screen
        self.settings = clint_game.settings
        self.screen_rect = clint_game.screen_rect
        self.gravity = clint_game.gravity
        self.direction_list = random.choice(clint_game.spawn_list)
        self.plus_minus = random.choice([-1, 1])
        self.screen_width = clint_game.screen_width
        self.screen_height = clint_game.screen_height

        self.original_image = pygame.image.load("images/enemies/bomb/bomb.png")
        self.image = pygame.transform.scale(
            self.original_image, (0.06 * self.screen_height, 0.06 * self.screen_height),
        ).convert_alpha()

        self.original_image2 = pygame.image.load("images/enemies/bomb/explosion.png")
        self.image2 = pygame.transform.scale(
            self.original_image2,
            (0.11 * self.screen_height, 0.11 * self.screen_height),
        ).convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = self.screen_rect.centerx
        self.rect.top = self.screen_rect.top

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.gravity + 0.00563 * self.screen_height

        self.x += self.direction_list * self.plus_minus
        self.rect.y = self.y
        self.rect.x = self.x

    def animate_anvil(self):
        if self.anvil_index > 3:
            self.anvil_index = 0

        self.flying_image = self.anvil_fly[int(self.anvil_index)]

        self.anvil_index += 0.1

    def blitme(self):
        if self.rect.bottom < int(0.83 * self.screen_height):
            self.screen.blit(self.image, self.rect)
        else:
            self.screen.blit(self.image2, self.rect)

