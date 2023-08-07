import pygame
from pygame.sprite import Sprite


class GunBonus(Sprite):
    def __init__(self, clint_game):
        super().__init__()
        self.screen = clint_game.screen
        self.screen_rect = clint_game.screen_rect
        self.game_speed = clint_game.settings.game_speed
        self.screen_width = clint_game.screen_width
        self.screen_height = clint_game.screen_height
        self.ground_level = clint_game.grass_y - 0.23 * self.screen_height

        self.original_image = pygame.image.load("images/bonuses/gun_bonus.png")
        self.image = pygame.transform.scale(
            self.original_image, (0.06 * self.screen_height, 0.06 * self.screen_height)
        ).convert_alpha()
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()

        self.rect.left = self.screen_rect.right
        self.rect.y = self.ground_level

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x -= self.game_speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)
