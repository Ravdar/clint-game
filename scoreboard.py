import pygame
from pygame.sprite import Group
from lifes import Life
import json


class Scoreboard:
    def __init__(self, clint_game):
        self.screen = clint_game.screen
        self.settings = clint_game.settings
        self.stats = clint_game.stats
        self.screen_rect = self.screen.get_rect()

        self.text_color = (0, 0, 0)
        self.font = pygame.font.Font("fonts/ArcadeClassic.ttf", 48)
        self.font2 = pygame.font.Font("fonts/ArcadeClassic.ttf", 28)

    def prep_high_score(self):
        with open("high_score.json", "r") as f:
            self.high_score = json.load(f)
            self.high_score = str(self.high_score["high_score"])

    def save_high_score(self):
        with open("high_score.json") as f:
            my_data = json.load(f)
        my_data["high_score"] = self.high_score
        with open("high_score.json", "w") as f:
            json.dump(my_data, f)

    def current_score(self):
        score = str(self.stats.score)
        self.score_image = self.font.render(score, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.screen_rect.top + 20

        self.high_score_image = self.font2.render(
            self.high_score, True, self.text_color
        )
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.score_rect.centerx
        self.high_score_rect.top = self.score_rect.bottom + 20

    def show_current_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        if int(self.high_score) < int(self.stats.score):
            self.high_score = str(self.stats.score)

        self.screen.blit(self.high_score_image, self.high_score_rect)

    def drunk_label(self):
        self.drunk_label_image = self.font2.render(
            "You are drunk!", True, (255, 255, 255)
        )
        self.drunk_label_rect = self.drunk_label_image.get_rect()
        self.drunk_label_rect.centerx = self.screen_rect.centerx
        self.drunk_label_rect.bottom = 350

    def show_drunk_label(self):
        self.screen.blit(self.drunk_label_image, self.drunk_label_rect)

    def flash_label(self):
        self.flash_label_image = self.font2.render(
            "Mega speed and jump!", True, (255, 255, 255)
        )
        self.flash_label_rect = self.flash_label_image.get_rect()
        self.flash_label_rect.centerx = self.screen_rect.centerx
        self.flash_label_rect.bottom = 330

    def show_flash_label(self):
        self.screen.blit(self.flash_label_image, self.flash_label_rect)

    def gun_label(self):
        self.gun_label_image = self.font2.render(
            "You can shoot those bastards!", True, (255, 255, 255)
        )
        self.gun_label_rect = self.gun_label_image.get_rect()
        self.gun_label_rect.centerx = self.screen_rect.centerx
        self.gun_label_rect.bottom = 370

    def show_gun_label(self):
        self.screen.blit(self.gun_label_image, self.gun_label_rect)
