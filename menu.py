import pygame
import math


class Menu:
    def __init__(self, clint_game):
        self.screen = clint_game.screen
        self.screen_rect = self.screen.get_rect()
        self.screen_width = clint_game.screen_width
        self.screen_height = clint_game.screen_height
        self.score = clint_game.stats.score
        self.clock = pygame.time.Clock()

        self.color = (227, 209, 34)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.Font("fonts/8BitOperatorPlus8-Bold.ttf", 48)
        self.title_font = pygame.font.Font("fonts/deadsaloon.ttf", 84)

        self.rect = pygame.Rect(0, 0, self.screen_width, self.screen_height)
        self.rect.center = self.screen_rect.center

        self.rect_go = pygame.Surface(
            (int(self.screen_width) * 8 / 10, int(self.screen_height) * 8 / 10)
        )
        self.rect_go.set_alpha(128)

        # Blood

        self.blood_original_image = pygame.image.load("images/others/blood/blood.png")
        self.blood_image = pygame.transform.scale(
            self.blood_original_image, (100, 100)
        ).convert_alpha()
        self.blood_image.set_colorkey((0, 0, 0))

        self.blood_rect = self.blood_image.get_rect()
        self.blood_rect.top = self.screen_rect.top
        self.blood_rect.left = self.screen_rect.left + 200

        self.drop_1_image = pygame.image.load("images/others/blood/drop_1.png")
        self.drop_1_image = pygame.transform.scale(
            self.drop_1_image, (100, 100)
        ).convert_alpha()

        self.drop_1_rect = self.drop_1_image.get_rect()
        self.drop_1_rect.top = self.screen_rect.top
        self.drop_1_rect.left = self.screen_rect.left + 200

        self.drop_2_image = pygame.image.load("images/others/blood/drop_2.png")
        self.drop_2_image = pygame.transform.scale(
            self.drop_2_image, (100, 100)
        ).convert_alpha()

        self.drop_2_rect = self.drop_2_image.get_rect()
        self.drop_2_rect.top = self.screen_rect.top
        self.drop_2_rect.left = self.screen_rect.left + 200

        self.drop_3_image = pygame.image.load("images/others/blood/drop_3.png")
        self.drop_3_image = pygame.transform.scale(
            self.drop_3_image, (100, 100)
        ).convert_alpha()

        self.drop_3_rect = self.drop_3_image.get_rect()
        self.drop_3_rect.top = self.screen_rect.top
        self.drop_3_rect.left = self.screen_rect.left + 200

        # Andrew

        self.andrew_walk_1 = pygame.image.load("images/others/andrew/andrew_walk_1.png")
        self.andrew_walk_1 = pygame.transform.scale(
            self.andrew_walk_1, (130, 90)
        ).convert_alpha()

        self.andrew_walk_2 = pygame.image.load("images/others/andrew/andrew_walk_2.png")
        self.andrew_walk_2 = pygame.transform.scale(
            self.andrew_walk_2, (130, 90)
        ).convert_alpha()

        self.andrew_walk = [self.andrew_walk_1, self.andrew_walk_2]
        self.andrew_index = 1
        self.andrew_image = self.andrew_walk[int(self.andrew_index)]

        self.andrew_rect = self.andrew_walk_1.get_rect()
        self.andrew_rect.centerx = self.screen_rect.centerx + 150
        self.andrew_rect.centery = self.rect.centery - 200

    def prep_message(self, msg, y):
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.right = self.screen_rect.right * 5 / 6
        self.msg_image_rect.centery = self.rect.centery + y
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def prep_go_message(self, msg, y):
        self.msg_image = self.font.render(msg, True, self.text_color).convert_alpha()
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.centerx = self.rect.centerx
        self.msg_image_rect.centery = self.rect.centery + y
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def prep_title_message(self, msg, y):
        self.msg_image = self.title_font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.centerx = self.screen_rect.centerx + 150
        self.msg_image_rect.centery = self.rect.centery + y
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def display_menu(self):
        self.menu_start_time = pygame.time.get_ticks()
        self.screen.fill(self.color, self.rect)
        self.prep_message("Start", 100)
        self.prep_message("Options", 150)
        self.prep_message("Highscores", 200)
        self.prep_message("Legend", 250)
        self.prep_message("Exit", 300)
        self.prep_title_message("Clint Adventures", -300)
        self.prep_title_message("The mystery of King Scorpio", -100)
        self.screen.blit(self.andrew_image, self.andrew_rect)
        self.screen.blit(self.blood_image, self.blood_rect)

    def display_game_over(self, score):
        self.rect_go.fill((255, 0, 0, 128))
        self.rect_go.set_alpha(128)
        self.screen.blit(
            self.rect_go,
            (self.screen_rect.right * 1 / 10, self.screen_rect.bottom * 1 / 10),
        )
        self.prep_go_message("Game over", -100)
        self.prep_go_message(f"you've scored  {score} points", -50)
        self.prep_go_message("press 's' to start again", 100)
        self.prep_go_message("press 'm' to go to menu", 150)

    def drop_1_animation(self):
        self.drop_1_height = self.drop_1_image.get_height()
        self.drop_1_image = pygame.transform.scale(
            self.drop_1_image, (100, self.drop_1_height + 1)
        ).convert_alpha()
        self.screen.blit(self.drop_1_image, self.drop_1_rect)

    def drop_2_animation(self):
        self.drop_2_height = self.drop_2_image.get_height()
        self.drop_2_image = pygame.transform.scale(
            self.drop_2_image, (100, self.drop_2_height + 3)
        ).convert_alpha()
        self.screen.blit(self.drop_2_image, self.drop_2_rect)

    def drop_3_animation(self):
        self.drop_3_height = self.drop_3_image.get_height()
        self.drop_3_image = pygame.transform.scale(
            self.drop_3_image, (100, self.drop_3_height + 1)
        ).convert_alpha()
        self.screen.blit(self.drop_3_image, self.drop_3_rect)

    def andrew_animation(self):
        self.andrew_rect.x += 5

        if self.andrew_index > 2:
            self.andrew_index = 0

        self.andrew_image = self.andrew_walk[int(self.andrew_index)]

        self.andrew_index += 0.2

    #     self.andrew_image = pygame.image.load("images/andrew.png")
    #     # self.andrew_image.set_colorkey((255, 0, 255))

    #     self.andrew_height = 30
    #     self.andrew_width = 15

    #     self.andrew_rect = self.andrew_image.get_rect()

    #     while True:

    #         dt = self.clock.tick(60) / 1000.0
    #         scale = (
    #             math.sin(pygame.time.get_ticks() / 1000.0 * 2 * math.pi) + 1
    #         ) / 2 + 0.5
    #         scaled_size = (
    #             int(self.andrew_width * scale),
    #             int(self.andrew_height * scale),
    #         )
    #         self.andrew_image = pygame.transform.scale(
    #             self.andrew_image, scaled_size
    #         ).convert_alpha()
    #         # self.andrew_image.set_colorkey((255, 0, 255))
    #         print(scaled_size)
    #         print(
    #             (750 - scaled_size[0]) / 2, (450 - scaled_size[1]) / 2,
    #         )
    #         self.screen.blit(
    #             self.andrew_image,
    #             ((750 - scaled_size[0]) / 2, (450 - scaled_size[1]) / 2,),
    #         )

    # #     # if self.andrew_height >= 1450:
    # #     #     print(self.andrew_height)
    # #     #     self.andrew_height = 1450
    # #     #     self.screen.blit(self.andrew_image, self.andrew_rect)
    # #     # else:
    # #     self.x += 1
    # #     print(self.x)

    # #     if self.x % 500 == 0:
    # #         self.xx = 2

    # #     print(self.x)
    # #     print(self.andrew_height)
    # #     self.andrew_image = pygame.transform.scale(
    # #         self.andrew_original_image,
    # #         (self.andrew_width + self.xx, self.andrew_height + self.xx * 2),
    # #     ).convert_alpha()
    # #     self.andrew_image.set_colorkey((255, 0, 255))
    # #     self.screen.blit(self.andrew_image, self.andrew_rect)
    # #     self.xx = 0

    # # else:
    # #     self.andrew_height = self.andrew_image.get_height()
    # #     print(self.andrew_height)
    # #     self.x -= 0.01 * self.andrew_height
    # #     if self.x > 0:
    # #         self.x = self.x * (-1)
    # #     self.andrew_image = pygame.transform.scale(
    # #         self.andrew_original_image,
    # #         (self.andrew_width + self.x, self.andrew_height + 2 * self.x),
    # #     ).convert_alpha()
    # #     self.andrew_image.set_colorkey((255, 0, 255))
    # #     self.screen.blit(self.andrew_image, self.andrew_rect)
    # #     if self.andrew_height <= 30:
    # #         self.bigger = True

