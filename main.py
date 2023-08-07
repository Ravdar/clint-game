import random
import time
import sys
import pygame

from settings import Settings
from clint import Clint
from cloud import Cloud
from bullet import Bullet
from eagle import Eagle
from cactus import Cactus
from game_stats import GameStats
from scoreboard import Scoreboard
from lifes import Life
from menu import Menu
from bandit import Bandit
from bomb import Bomb
from tequilla import Tequilla
from goat import Goat
from horse import Horse
from background import Background
from flash import Flash
from life_bonus import LifeBonus
from gun_bonus import GunBonus
from clint_bullet import ClintBullet


class ClintGame:
    def __init__(self):
        """Initialisation of game"""
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Clint Adventures: The mystery of King Scorpion")
        info = pygame.display.Info()
        self.icon = pygame.image.load("images/others/andrew/andrew_icon.png")
        pygame.display.set_icon(self.icon)
        self.running = True

        self.initial_time = pygame.time.get_ticks()
        self.screen_rect = self.screen.get_rect()
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        print(self.screen_width)
        print(self.screen_height)
        self.ground = pygame.Surface((self.screen_width, self.screen_height / 8))
        self.grass = pygame.Surface((self.screen_width, self.screen_height / 24))
        self.grass_y = (
            self.screen_height - self.ground.get_height() - self.grass.get_height()
        )

        self.settings = Settings()
        self.bullets = pygame.sprite.Group()
        self.eagles = pygame.sprite.Group()
        self.cactuses = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.lifes = pygame.sprite.Group()
        self.bandits = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.tequillas = pygame.sprite.Group()
        self.goats = pygame.sprite.Group()
        self.bgs = pygame.sprite.Group()
        self.flashes = pygame.sprite.Group()
        self.life_bons = pygame.sprite.Group()
        self.gun_bons = pygame.sprite.Group()
        self.clint_bullets = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        self.last_collision = 0
        self.gravity = self.settings.clint_gravity
        self.spawn_list = (
            [1] * 1
            + [2] * 4
            + [3] * 6
            + [4] * 8
            + [5] * 10
            + [6] * 9
            + [7] * 8
            + [8] * 7
            + [9] * 6
            + [10] * 5
        )

        self.stats = GameStats(self)
        self.menu = Menu(self)
        self.clint = Clint(self)
        self.horse = Horse(self)
        self.scoreboard = Scoreboard(self)
        self.bg = Background(self, self.screen_rect.left)
        self.bgs.add(self.bg)

        self.scoreboard.prep_high_score()
        self.scoreboard.current_score()
        self.bg.display_sun()
        self.create_bg()

        # Initial spawn of enemies
        self.next_cactus_spawn = (
            random.choice(self.spawn_list) * self.settings.spawn_pause
        )
        self.next_eagle_spawn = (
            random.choice(self.spawn_list) * self.settings.spawn_pause
        )
        self.next_bandit_spawn = (
            random.choice(self.spawn_list) * self.settings.spawn_pause
        )
        self.next_bomb_spawn = (
            random.choice(self.spawn_list) * self.settings.spawn_pause
        )
        self.next_goat_spawn = (
            random.choice(self.spawn_list) * self.settings.spawn_pause
        )
        self.next_cloud_spawn = (
            random.choice(self.spawn_list) * self.settings.spawn_pause
        )

        self.last_cactus_spawn = 0
        self.last_eagle_spawn = 0
        self.last_bandit_spawn = 0
        self.last_bomb_spawn = 0
        self.last_goat_spawn = 0
        self.last_cloud_spawn = 0

        # Importing sounds used in a game
        self.menu_music = pygame.mixer.Sound(
            "audio/DOXO - Under The Sun.wav"
        )  #  tutaj dać if last played < tyle ile trwa piosenka to nie grać dalel
        self.game_music = pygame.mixer.Sound("audio/DOXO - Stalion.wav")
        self.game_music.set_volume(0.75)
        self.shot_sound = pygame.mixer.Sound("audio/shot.wav")
        self.shot_sound.set_volume(0.5)
        self.dash_sound = pygame.mixer.Sound("audio/dash.wav")
        self.dash_sound.set_volume(0.6)
        self.bonus_sound = pygame.mixer.Sound("audio/bonus_pickup.wav")
        self.game_over_sound = pygame.mixer.Sound("audio/game_over.wav")
        self.life_loss_sound = pygame.mixer.Sound("audio/life_loss.mp3")
        self.eagle_sound = pygame.mixer.Sound("audio/eagle scream.mp3")
        self.explosion_sound = pygame.mixer.Sound("audio/explosion2.wav")

        # Playing meny music
        self.menu_music.play()

    def run_game(self):
        """Main game loop"""

        while self.running == True:
            self.current_time = pygame.time.get_ticks()
            self.check_events()
            # Check and reset various power-up states and timers
            if self.stats.game_active == True:
                if (
                    self.clint.drunk == True
                    and self.current_time - self.drunk_time > 2000
                ):
                    self.clint.drunk = False
                if (
                    self.clint.flash_state == True
                    and self.current_time - self.flash_time > 5000
                ):
                    self.clint.flash_state = False
                if (
                    self.clint.has_gun == True
                    and self.current_time - self.gun_time > 6000
                ):
                    self.clint.has_gun = False
                # Spawning
                if self.horse.gate_rect.x < 1600:
                    if self.current_time % 1125 == 0:
                        self.create_tequilla()
                    if self.current_time % 1333 == 0:
                        self.create_flash()
                    if self.current_time % 1251 == 0:
                        self.create_gun_bon()
                    if self.current_time % 2001 == 0:
                        self.create_life_bon()
                # Update game settings
                self.settings.game_speed += self.settings.speed_increase
                if self.settings.spawn_pause > 1000:
                    self.settings.spawn_pause -= self.settings.spawn_pause_decrease
                # Update game elements
                if self.stats.game_over == False:
                    self.update_bg()
                    self.clint.update()
                    self.horse.update()
                    self.update_bullets()
                    self.update_clouds()
                    self.update_cactuses()
                    self.update_eagles()
                    self.update_bandits()
                    self.update_bombs()
                    self.update_tequillas()
                    self.update_goats()
                    self.update_flashes()
                    self.update_life_bons()
                    self.update_gun_bons()
                    self.update_clint_bullets()

                if len(self.bgs.sprites()) > 2:
                    self.bgs.remove(self.bgs.sprites()[0])

            self.update_screen()

    def check_events(self):
        """Event handling loop"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
        pygame.display.update()
        self.clock.tick(60)

    def check_keydown_events(self, event):
        # Moving player
        if self.stats.game_over == False:
            if event.key == pygame.K_UP:
                self.clint.jump = True
            elif event.key == pygame.K_DOWN:
                self.clint.dash = True
                self.dash_sound.play()
            elif event.key == pygame.K_RIGHT:
                self.clint.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.clint.moving_left = True
            elif event.key == pygame.K_SPACE:
                self.fire_clint_bullet()
        # Start game
        if event.key == pygame.K_s:  # and self.stats.game_active == False:
            self.stats.game_active = True
            self.stats.game_over = False
            self.menu_music.stop()
            self.stats.reset_stats()
            self.settings.starting_settings()  # nie wiem co to robi
            self.scoreboard.save_high_score()  # i to
            self.scoreboard.current_score()  # i to
            self.game_music.stop()
            self.create_lifes()
            self.game_music.play()
        # Pause
        elif event.key == pygame.K_p:
            if self.stats.game_active == True:
                self.stats.game_active = False
            else:
                self.stats.game_active = True
        # Quit game
        elif event.key == pygame.K_q:
            self.quit()

    def check_keyup_events(self, event):
        if event.key == pygame.K_UP:
            self.clint.jump = False
        elif event.key == pygame.K_DOWN:
            self.clint.dash = False
        elif event.key == pygame.K_RIGHT:
            self.clint.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.clint.moving_left = False

    def update_screen(self):
        """Handle key up events"""

        self.screen.fill(self.settings.bg_color)
        for bg in self.bgs.sprites():
            bg.blit_bg()
        # Display ground and grass
        self.ground.fill(self.settings.ground_color)
        self.grass.fill(self.settings.grass_color)
        self.bg.display_sun()
        # Display game elements during active gameplay
        if self.stats.game_active == True:
            self.screen.blit(
                self.ground, (0, self.screen_height - self.ground.get_height())
            )
            self.screen.blit(self.grass, (0, self.grass_y))
            for cloud in self.clouds.sprites():
                cloud.blitme()
            for cactus in self.cactuses.sprites():
                cactus.blitme()
            for life in self.lifes.sprites():
                life.blitme()
            for bullet in self.bullets.sprites():
                bullet.blitme()
            for clint_bullet in self.clint_bullets.sprites():
                clint_bullet.blitme()
            for eagle in self.eagles.sprites():
                eagle.animate_eagle()
                eagle.blitme()
            for bandit in self.bandits.sprites():
                bandit.animate_bandit()
                bandit.blitme()
            for bomb in self.bombs.sprites():
                bomb.blitme()
            for tequilla in self.tequillas.sprites():
                tequilla.blitme()
            for goat in self.goats.sprites():
                goat.blitme()
            for flash in self.flashes.sprites():
                flash.blitme()
            for gun_bon in self.gun_bons.sprites():
                gun_bon.blitme()
            for life_bon in self.life_bons.sprites():
                life_bon.blitme()

            self.horse.blitme()
            self.clint.blitme(self.current_time, self.last_collision)
            self.scoreboard.show_current_score()

            if (
                self.current_time - self.last_collision
                <= self.settings.intouchable_time
            ):
                self.clint.hit_effect = True
            else:
                self.clint.hit_effect = False
            if self.clint.drunk == True:
                self.scoreboard.show_drunk_label()
            if self.clint.flash_state == True:
                self.scoreboard.show_flash_label()
            if self.clint.has_gun == True:
                self.scoreboard.show_gun_label()

            if self.stats.game_over == True:
                self.menu.display_game_over(self.stats.score)
            else:
                self.clint.animate_clint()
                self.horse.animate_horse()

        else:
            # Display menu animations and options
            self.menu.display_menu()
            if self.menu.menu_start_time - self.initial_time > 3000:
                self.menu.drop_3_animation()
            if self.menu.menu_start_time - self.initial_time > 5000:
                self.menu.drop_1_animation()
            if self.menu.menu_start_time - self.initial_time > 9000:
                self.menu.drop_2_animation()
            if self.menu.menu_start_time - self.initial_time > 12000:
                self.menu.andrew_animation()

        pygame.display.flip()

    def fire_bullet(self):
        """Create and fire enemy bullet"""

        new_bullet = Bullet(self)
        self.shot_sound.play()
        self.bullets.add(new_bullet)

    def update_bullets(self):
        """Updates enemy bullet position and collisions"""

        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.right <= self.screen_rect.left:
                self.bullets.remove(bullet)
        if self.current_time - self.last_collision >= self.settings.intouchable_time:
            if pygame.sprite.spritecollideany(self.clint, self.bullets):
                self.clint_hit()
                self.last_collision = pygame.time.get_ticks()

    def fire_clint_bullet(self):
        """Create and fire Clint's bullet"""

        if self.clint.has_gun == True:
            new_clint_bullet = ClintBullet(self)
            self.clint_bullets.add(new_clint_bullet)
            self.shot_sound.play()

    def update_clint_bullets(self):
        """Updates Clint's bullet position and collisions"""

        self.clint_bullets.update()
        for clint_bullet in self.clint_bullets.copy():
            if clint_bullet.rect.left >= self.screen_rect.right:
                self.clint_bullets.remove(clint_bullet)
            for obj in [
                self.cactuses,
                self.bandits,
                self.eagles,
                self.goats,
                self.bombs,
            ]:
                collided = pygame.sprite.spritecollideany(clint_bullet, obj)
                if collided:
                    collided.kill()
                    self.clint_bullets.remove(clint_bullet)

    def create_cloud(self):
        """Create a new cloud and adds it to the clouds group"""

        cloud = Cloud(self)
        self.last_cloud_spawn = pygame.time.get_ticks()
        self.next_cloud_spawn = random.choice(self.spawn_list) * 1000
        self.clouds.add(cloud)

    def update_clouds(self):
        """Updates clouds position and deletes clouds beyond the screen"""

        self.clouds.update()
        if self.current_time - self.last_cloud_spawn >= self.next_cloud_spawn:
            self.create_cloud()
        for cloud in self.clouds.copy():
            if cloud.rect.right <= 0:
                self.clouds.remove(cloud)
                self.stats.score += 2
                self.scoreboard.current_score()

    def create_cactus(self):
        """Create a new cactus and adds it to the cactuses group"""

        if self.horse.gate_rect.x < 1800:
            cactus = Cactus(self)
            self.last_cactus_spawn = pygame.time.get_ticks()
            self.next_cactus_spawn = (
                random.choice(self.spawn_list) * self.settings.spawn_pause
            )
            self.cactuses.add(cactus)

    def update_cactuses(self):
        """Updates cactuses position and deletes cactuses beyond the screen"""

        self.cactuses.update()
        if self.current_time - self.last_cactus_spawn >= self.next_cactus_spawn:
            self.create_cactus()
        for cactus in self.cactuses.copy():
            if cactus.rect.right <= 0:
                self.cactuses.remove(cactus)
                self.stats.score += 3
        if self.current_time - self.last_collision >= self.settings.intouchable_time:
            collided = pygame.sprite.spritecollideany(self.clint, self.cactuses)
            if collided:
                collided.kill()
                self.clint_hit()
                self.last_collision = pygame.time.get_ticks()

    def create_eagle(self):
        """Create a new eagle and adds it to the eagles group"""

        if self.horse.gate_rect.x < 0:
            eagle = Eagle(self)
            self.eagles.add(eagle)
            self.last_eagle_spawn = pygame.time.get_ticks()
            self.next_eagle_spawn = (
                random.choice(self.spawn_list) * self.settings.spawn_pause
            )
            self.eagle_sound.play()

    def update_eagles(self):
        """Updates eagles position and deletes eagles beyond the screen"""

        self.eagles.update()
        if self.current_time - self.last_eagle_spawn >= self.next_eagle_spawn:
            self.create_eagle()
        for eagle in self.eagles.copy():
            if eagle.rect.right <= 0:
                self.eagles.remove(eagle)
                self.stats.score += 3
        if self.current_time - self.last_collision >= self.settings.intouchable_time:
            collided = pygame.sprite.spritecollideany(self.clint, self.eagles)
            if collided:
                collided.kill()
                self.clint_hit()
                self.last_collision = pygame.time.get_ticks()

    def create_bandit(self):
        """Create a new bandit and adds it to the bandits group"""

        if self.horse.gate_rect.x < -900:
            bandit = Bandit(self)
            self.bandits.add(bandit)
            self.last_bandit_spawn = pygame.time.get_ticks()
            self.next_bandit_spawn = (
                random.choice(self.spawn_list) * self.settings.spawn_pause
            )

    def update_bandits(self):
        """Updates bandits position and deletes bandits beyond the screen"""

        self.bandits.update()
        if self.current_time - self.last_bandit_spawn >= self.next_bandit_spawn:
            self.create_bandit()
        for bandit in self.bandits.copy():
            if bandit.x > 1000 and self.current_time % 100 == 0:
                self.fire_bullet()
            if bandit.rect.right <= 0:
                self.bandits.remove(bandit)
                self.stats.score += 5
        if self.current_time - self.last_collision >= self.settings.intouchable_time:
            collided = pygame.sprite.spritecollideany(self.clint, self.bandits)
            if collided:
                collided.kill()
                self.clint_hit()
                self.last_collision = pygame.time.get_ticks()

    def create_bomb(self):
        """Create a new bomb and adds it to the bomb group"""

        if self.horse.gate_rect.x < 1900:
            bomb = Bomb(self)
            self.bombs.add(bomb)
            self.last_bomb_spawn = pygame.time.get_ticks()
            self.next_bomb_spawn = (
                random.choice(self.spawn_list) * self.settings.spawn_pause
            )

    def update_bombs(self):
        """Updates bombs position and deletes bombs beyond the screen"""

        self.bombs.update()
        if self.current_time - self.last_bomb_spawn >= self.next_bomb_spawn:
            self.create_bomb()
        for bomb in self.bombs.copy():
            if bomb.rect.top >= self.grass_y:
                self.explosion_sound.play()
                self.bombs.remove(bomb)
                self.stats.score += 3
        if self.current_time - self.last_collision >= self.settings.spawn_pause:
            collided = pygame.sprite.spritecollideany(self.clint, self.bombs)
            if collided:
                collided.kill()
                self.clint_hit()
                self.last_collision = pygame.time.get_ticks()

    def create_tequilla(self):
        """Create a new tequilla bonus and adds it to the tequillas group"""

        tequilla = Tequilla(self)
        self.tequillas.add(tequilla)

    def update_tequillas(self):
        """Updates tequillas position and deletes tequillas beyond the screen"""

        self.tequillas.update()
        for tequilla in self.tequillas.sprites():
            if tequilla.rect.right <= 0:
                self.tequillas.remove(tequilla)
        collided = pygame.sprite.spritecollideany(self.clint, self.tequillas)
        if collided:
            self.clint.drunk = True
            self.bonus_sound.play()
            self.scoreboard.drunk_label()
            self.drunk_time = pygame.time.get_ticks()
            collided.kill()

    def create_flash(self):
        """Create a new flash bonus and adds it to the flashes group"""

        flash = Flash(self)
        self.flashes.add(flash)

    def update_flashes(self):
        """Updates flashes position and deletes flashes beyond the screen"""

        self.flashes.update()
        for flash in self.flashes.sprites():
            if flash.rect.right <= 0:
                self.flashes.remove(flash)
        collided = pygame.sprite.spritecollideany(self.clint, self.flashes)
        if collided:
            self.bonus_sound.play()
            self.clint.flash_state = True
            self.scoreboard.flash_label()
            self.flash_time = pygame.time.get_ticks()
            collided.kill()

    def create_life_bon(self):
        """Create a new life bonus and adds it to the clouds group"""

        life_bon = LifeBonus(self)
        self.life_bons.add(life_bon)

    def update_life_bons(self):
        """Updates life bons position and deletes life bons beyond the screen"""

        self.life_bons.update()
        for life_bon in self.life_bons.sprites():
            if life_bon.rect.right <= 0:
                self.life_bons.remove(life_bon)
        collided = pygame.sprite.spritecollideany(self.clint, self.life_bons)
        if collided:
            if len(self.lifes.sprites()) < 3:
                self.bonus_sound.play()
                self.stats.lifes_left += 1
                life = Life(self)
                self.lifes.add(life)
                life.rect.left = self.screen_rect.left + 40 * (
                    len(self.lifes.sprites()) - 1
                )
                life.rect.bottom = self.screen_rect.bottom - 25
                collided.kill()

    def create_gun_bon(self):
        """Create a new gun bonus and adds it to the guns group"""

        gun_bon = GunBonus(self)
        self.gun_bons.add(gun_bon)

    def update_gun_bons(self):
        """Updates gun bons position and deletes gun bons beyond the screen"""

        self.gun_bons.update()
        for gun_bon in self.gun_bons.sprites():
            if gun_bon.rect.right <= 0:
                self.gun_bons.remove(gun_bon)
        collided = pygame.sprite.spritecollideany(self.clint, self.gun_bons)
        if collided:
            self.bonus_sound.play()
            self.clint.has_gun = True
            self.scoreboard.gun_label()
            self.gun_time = pygame.time.get_ticks()
            collided.kill()

    def create_goat(self):
        """Create a new goat and adds it to the goats group"""

        if self.horse.gate_rect.x < -1600:
            goat = Goat(self)
            self.goats.add(goat)
            self.last_goat_spawn = pygame.time.get_ticks()
            self.next_goat_spawn = (
                random.choice(self.spawn_list) * self.settings.spawn_pause
            )

    def update_goats(self):
        """Updates goats position and deletes goats beyond the screen"""

        self.goats.update()
        if self.current_time - self.last_goat_spawn >= self.next_goat_spawn:
            self.create_goat()
        for goat in self.goats.copy():
            if goat.rect.right <= 0:
                self.goats.remove(goat)
                self.stats.score += 3
        if self.current_time - self.last_collision >= self.settings.intouchable_time:
            collided = pygame.sprite.spritecollideany(self.clint, self.goats)
            if collided:
                collided.kill()
                self.clint_hit()
                self.last_collision = pygame.time.get_ticks()

    def create_bg(self):
        """Generates a new background part and adds it to the backgrounds group"""

        bg = Background(self, self.screen_rect.right)
        self.bgs.add(bg)

    def update_bg(self):
        """Handles background"""

        self.bgs.update()
        if self.bgs.sprites()[0].bg_rect.right < 4:
            self.create_bg()
        for bg in self.bgs.copy():
            if bg.bg_rect.right <= 0:
                self.bgs.remove(bg)

    def create_lifes(self):
        """Manages lifes left icons"""

        for lifes_number in range(self.stats.lifes_left):
            life = Life(self)
            self.lifes.add(life)
            life.rect.left = self.screen_rect.left + 40 * lifes_number
            life.rect.bottom = self.screen_rect.bottom - 25

    def clint_hit(self):
        """Handle player getting hit"""

        self.stats.lifes_left -= 1
        if self.stats.lifes_left > -1:
            self.lifes.remove(self.lifes.sprites()[-1])
            self.life_loss_sound.play()
        else:
            self.stats.game_over = True
            self.game_music.stop()
            self.game_over_sound.play()

    def quit(self):
        """Quit the game"""

        pygame.quit()
        sys.exit()


# Main entry point
if __name__ == "__main__":
    clint_game = ClintGame()
    clint_game.run_game()
