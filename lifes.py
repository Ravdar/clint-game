import pygame
from pygame.sprite import Sprite


class Life(Sprite):
    def __init__(self, clint_game):
        super().__init__()
        self.screen = clint_game.screen
        self.settings = clint_game.settings
        self.screen_rect = clint_game.screen.get_rect()
        self.stats = clint_game.stats

        self.image = pygame.image.load("images/others/life.bmp")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.left = self.screen_rect.left + 30
        self.rect.bottom = self.screen_rect.bottom - 30
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

