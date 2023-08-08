import pygame
from pygame.sprite import Sprite


class Bandit(Sprite):
    def __init__(self, clint_game):
        super().__init__()
        self.screen = clint_game.screen
        self.settings = clint_game.settings
        self.screen_rect = clint_game.screen.get_rect()
        self.screen_width = clint_game.screen_width
        self.screen_height = clint_game.screen_height

        self.original_image = pygame.image.load(
            "images/enemies/bandit/bandit_walk1.png"
        )
        self.image = pygame.transform.scale(
            self.original_image, (0.041 * self.screen_width, 0.11 * self.screen_height)
        ).convert_alpha()
        self.image.set_colorkey((255, 255, 255))

        self.original_image2 = pygame.image.load(
            "images/enemies/bandit/bandit_walk2.png"
        )
        self.image2 = pygame.transform.scale(
            self.original_image2, (0.041 * self.screen_width, 0.11 * self.screen_height)
        ).convert_alpha()
        self.image2.set_colorkey((255, 255, 255))

        self.original_image3 = pygame.image.load(
            "images/enemies/bandit/bandit_walk3.png"
        )
        self.image3 = pygame.transform.scale(
            self.original_image3, (0.041 * self.screen_width, 0.11 * self.screen_height)
        ).convert_alpha()
        self.image3.set_colorkey((255, 255, 255))

        self.bandit_index = 0
        self.bandit_walk = [self.image, self.image3, self.image2, self.image3]
        self.walking_image = self.bandit_walk[int(self.bandit_index)]
        self.rect = self.image.get_rect()

        self.rect.left = self.screen_rect.right
        self.rect.bottom = 0.856 * self.screen_height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x -= self.settings.game_speed + 2
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.walking_image, self.rect)

    def animate_bandit(self):
        self.bandit_index += 0.1

        if self.bandit_index > 4:
            self.bandit_index = 0

        self.walking_image = self.bandit_walk[int(self.bandit_index)]

