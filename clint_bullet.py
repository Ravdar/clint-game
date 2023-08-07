import pygame
from pygame.sprite import Sprite


class ClintBullet(Sprite):
    def __init__(self, clint_game):
        super().__init__()
        self.screen = clint_game.screen
        self.settings = clint_game.settings
        self.clint = clint_game.clint
        self.color = (255, 255, 0)
        self.original_image = pygame.image.load("images/clint/clint_bullet.png")
        self.image = pygame.transform.scale(self.original_image, (25, 18),)
        self.image = self.image.convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.midleft = self.clint.rect.midright

        self.x = float(self.rect.x)

    def update(self):
        self.x += self.settings.game_speed + 11
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)
