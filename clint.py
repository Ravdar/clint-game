import pygame


class Clint:
    def __init__(self, clint_game):
        self.screen = clint_game.screen
        self.settings = clint_game.settings
        self.screen_rect = clint_game.screen_rect
        self.gravity = clint_game.gravity
        self.screen_width = clint_game.screen_width
        self.screen_height = clint_game.screen_height
        self.ground_level = clint_game.grass_y - 0.079 * self.screen_height
        self.game_over = clint_game.stats.game_over

        self.original_image = pygame.image.load("images/clint/clint_walk1.png")
        self.image = pygame.transform.scale(
            self.original_image, (0.035 * self.screen_width, 0.11 * self.screen_height)
        )
        self.image = self.image.convert_alpha()
        self.image.set_colorkey((255, 255, 255))

        self.original_image2 = pygame.image.load("images/clint/clint_walk2.png")
        self.image2 = pygame.transform.scale(
            self.original_image2, (0.035 * self.screen_width, 0.11 * self.screen_height)
        )
        self.image2 = self.image2.convert_alpha()
        self.image2.set_colorkey((255, 255, 255))

        self.original_image3 = pygame.image.load("images/clint/clint_walk3.png")
        self.image3 = pygame.transform.scale(
            self.original_image3, (0.035 * self.screen_width, 0.11 * self.screen_height)
        )
        self.image3 = self.image3.convert_alpha()
        self.image3.set_colorkey((255, 255, 255))

        self.original_image4 = pygame.image.load("images/clint/clint_jump.png")
        self.image4 = pygame.transform.scale(
            self.original_image4, (0.041 * self.screen_width, 0.11 * self.screen_height)
        )
        self.image4 = self.image4.convert_alpha()
        self.image4.set_colorkey((255, 255, 255))

        self.original_image5 = pygame.image.load("images/clint/clint_dash.png")
        self.image5 = pygame.transform.scale(
            self.original_image5, (0.035 * self.screen_width, 0.11 * self.screen_height)
        )
        self.image5 = self.image5.convert_alpha()
        self.image5.set_colorkey((255, 255, 255))

        self.clint_walk = [self.image, self.image3, self.image2, self.image3]
        self.clint_index = 0
        self.walking_image = self.clint_walk[int(self.clint_index)]

        self.rect = self.walking_image.get_rect()
        self.rect.bottomleft = (0.051 * self.screen_width, 0.67 * self.screen_height)
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

        self.jump = False
        self.dash = False
        self.drunk = False
        self.flash_state = False
        self.has_gun = False

        self.jump_sound = pygame.mixer.Sound("audio/jump.wav")

        #  Hit effect
        self.hit_effect = False
        self.hit_color = (255, 0, 0)
        self.hit_rect = pygame.Surface(
            (int(self.screen_width), int(self.screen_height))
        )
        self.hit_rect.fill(self.hit_color)
        self.hit_rect.set_alpha(100)
        self.last_blit = 0

    def update(self):
        self.gravity += 0.7 / 1080 * self.screen_height
        self.y += self.gravity

        if self.flash_state == True:

            if self.moving_right == True and self.rect.right < self.screen_rect.right:
                self.x += self.settings.clint_speed + 0.0026 * self.screen_width
            if self.moving_left == True and self.rect.left > 0:
                self.x -= self.settings.clint_speed + 0.0026 * self.screen_width

            if self.dash == True and self.rect.bottom < self.screen_rect.bottom:
                self.y += self.settings.clint_speed + 0.0026 * self.screen_width

            if self.jump == True and self.y > self.ground_level:
                self.gravity = -0.02315 * self.screen_height
                self.jump_sound.play()

            if self.y > self.ground_level:
                self.y = self.ground_level
                if self.jump == False:
                    self.gravity = 0.00185 * self.screen_height

        elif self.drunk == True:

            if self.moving_left == True and self.rect.right < self.screen_rect.right:
                self.x += self.settings.clint_speed
            if self.moving_right == True and self.rect.left > 0:
                self.x -= self.settings.clint_speed

            if self.jump == True and self.rect.bottom < self.screen_rect.bottom:
                self.y += self.settings.clint_speed

            if self.dash == True and self.y > self.ground_level:
                self.gravity = -0.0166 * self.screen_height
                self.jump_sound.play()

            if self.y > self.ground_level:
                self.y = self.ground_level
                if self.dash == False:
                    self.gravity = -0.0166 * self.screen_height

        else:

            if self.moving_right == True and self.rect.right < self.screen_rect.right:
                self.x += self.settings.clint_speed
            if self.moving_left == True and self.rect.left > 0:
                self.x -= self.settings.clint_speed

            if self.dash == True and self.rect.bottom < self.screen_rect.bottom:
                self.y += self.settings.clint_speed

            if self.jump == True and self.y > self.ground_level:
                self.gravity = -0.0166 * self.screen_height
                self.jump_sound.play()

            if self.y > self.ground_level:
                self.y = self.ground_level
                if self.jump == False:
                    self.gravity = 0.00185 * self.screen_height

        self.rect.y = self.y
        self.rect.x = self.x

    def blitme(self, current_time, last_collision):
        if self.hit_effect == True and self.game_over == False:
            if current_time - last_collision < 150:
                self.screen.blit(self.hit_rect, (0, 0))
            if current_time - self.last_blit > 25:
                if self.jump == True:
                    self.screen.blit(self.image4, self.rect)
                    self.last_blit = pygame.time.get_ticks()
                elif self.dash == True:
                    self.screen.blit(self.image5, self.rect)
                    self.last_blit = pygame.time.get_ticks()
                else:
                    self.screen.blit(self.walking_image, self.rect)
                    self.last_blit = pygame.time.get_ticks()

        else:

            if self.jump == True:
                self.screen.blit(self.image4, self.rect)
            elif self.dash == True:
                self.screen.blit(self.image5, self.rect)
            else:
                self.screen.blit(self.walking_image, self.rect)

    def starting_position(self):
        self.x = self.screen_rect.left
        self.rect.x = self.x

    def animate_clint(self):

        if self.clint_index >= 4:
            self.clint_index = 0

        if self.jump == False and self.dash == False:

            self.walking_image = self.clint_walk[int(self.clint_index)]

            if self.moving_left == True or self.moving_right == True:
                self.clint_index += 0.3
            else:
                self.clint_index += 0.1
