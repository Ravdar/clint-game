import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, clint_game):
        super().__init__()
        self.screen = clint_game.screen
        self.settings = clint_game.settings
        self.color = (255, 255, 0)
        self.original_image = pygame.image.load(
            "images/enemies/bandit/bandit_bullet.png"
        )
        self.image = pygame.transform.scale(self.original_image, (25, 18),)
        self.image = self.image.convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        for bandit in clint_game.bandits:
            self.rect.midleft = bandit.rect.midleft

        self.x = float(self.rect.x)

    def update(self):
        self.x -= self.settings.bullet_speed + self.settings.game_speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)
