import pygame
from pygame.sprite import Sprite


class Goat(Sprite):
    def __init__(self, clint_game):
        super().__init__()
        self.screen = clint_game.screen
        self.settings = clint_game.settings
        self.screen_rect = self.screen.get_rect()
        self.gravity = clint_game.settings.goat_gravity
        self.screen_width = clint_game.screen_width
        self.screen_height = clint_game.screen_height

        self.image = pygame.image.load("images/enemies/goat.png")
        self.image = pygame.transform.scale(
            self.image, (0.1 * self.screen_height, 0.1 * self.screen_height)
        )
        self.image = self.image.convert()
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.left = self.screen_rect.right
        self.rect.bottom = 0.845 * self.screen_height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.gravity += 0.5
        self.y += self.gravity
        self.x -= self.settings.game_speed + 2

        if self.rect.y >= 0.833 * self.screen_height:
            self.jump = True
            self.gravity = 2
            self.gravity -= 22

        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)
