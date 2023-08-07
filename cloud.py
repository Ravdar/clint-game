import pygame
from pygame.sprite import Sprite
import random


class Cloud(Sprite):
    def __init__(self, clint_game):
        super().__init__()
        self.screen = clint_game.screen
        self.settings = clint_game.settings
        self.screen_rect = self.screen.get_rect()

        self.cloud_x_rects = [num for num in range(100, 201)]
        self.cloud_sizes = [num for num in range(50, 101)]

        self.spawn = random.choice(self.cloud_x_rects)
        self.size = random.choice(self.cloud_sizes)

        self.original_image = pygame.image.load("images/others/bg/cloud_1.png")
        self.image = pygame.transform.scale(
            self.original_image, (2 * self.size, self.size)
        )
        self.image1 = self.image.convert()
        self.image1.set_colorkey((0, 0, 0))

        self.original_image2 = pygame.image.load("images/others/bg/cloud_2.png")
        self.image2 = pygame.transform.scale(
            self.original_image2, (2 * self.size, self.size)
        )
        self.image2 = self.image.convert()
        self.image2.set_colorkey((0, 0, 0))

        self.cloud_images = [self.image1, self.image2]

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.screen_rect.right, self.spawn)
        self.x = float(self.rect.x)

    def update(self):
        self.x -= self.settings.game_speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)

