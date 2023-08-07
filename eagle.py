import pygame
from pygame.sprite import Sprite


class Eagle(Sprite):
    def __init__(self, clint_game):
        super().__init__()
        self.screen = clint_game.screen
        self.settings = clint_game.settings
        self.screen_rect = self.screen.get_rect()
        self.screen_width = clint_game.screen_width
        self.screen_height = clint_game.screen_height
        self.ground_level = clint_game.grass_y - 0.243 * self.screen_height

        self.image = pygame.image.load("images/enemies/eagle/eagle.png")
        self.image = pygame.transform.scale(
            self.image, (0.110 * self.screen_height, 0.150 * self.screen_height)
        ).convert_alpha()
        self.image.set_colorkey((0, 0, 0))

        self.image2 = pygame.image.load("images/enemies/eagle/eagle2.png")
        self.image2 = pygame.transform.scale(
            self.image2, (0.110 * self.screen_height, 0.150 * self.screen_height)
        ).convert_alpha()
        self.image2.set_colorkey((0, 0, 0))

        self.eagle_fly = [self.image, self.image2]
        self.eagle_index = 0
        self.flying_image = self.eagle_fly[int(self.eagle_index)]

        self.rect = self.image.get_rect()
        self.rect.left = self.screen_rect.right
        self.rect.y = self.ground_level
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x -= self.settings.game_speed + 2
        self.rect.x = self.x

    def animate_eagle(self):
        if self.eagle_index > 2:
            self.eagle_index = 0

        self.flying_image = self.eagle_fly[int(self.eagle_index)]

        self.eagle_index += 0.1

    def blitme(self):
        self.screen.blit(self.flying_image, self.rect)
