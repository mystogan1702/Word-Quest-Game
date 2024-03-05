import time

import pygame.transform
import button

from pygame.image import load
from settings import *
from level import Level
from player import Player
from world import World
from Health import HealthBar


class Game:
    def __init__(self):
        self.game_paused = True
        self.playing = False
        self.menu_state = "main"
        self.muted = muted
        self.current_stage = Level()
        self.screen = pygame.display.set_mode(windowSize)
        self.click = 0
        self.click_paused = 0
        self.has_gender = False
        self.movement = [False, False]
        self.gender = 'boy'
        self.game_status = "adventure"
        self.has_gender = False
        self.world = World(world_data)
        self.player = Player('player', self.gender, 250, 520, 0.15, 3)
        self.health = HealthBar(5, 5, self.player.health, self.player.max_health)
        self.screen_scroll = 0

        surf = load('assets/bg and cursor/Cursor.png').convert_alpha()
        width = surf.get_width()
        height = surf.get_height()
        cursor_img = pygame.transform.scale(surf, (int(width * 0.5), int(height * 0.5)))
        cursor = pygame.cursors.Cursor((0, 0), cursor_img)
        pygame.mouse.set_cursor(cursor)

        self.play_img = load('assets/buttons/play.png').convert_alpha()
        self.quit_img = load('assets/buttons/Quit.png').convert_alpha()
        self.settings_img = load('assets/buttons/Settings.png').convert_alpha()
        self.back_img = load('assets/buttons/Back.png').convert_alpha()
        self.audio_img = load('assets/buttons/Audio.png').convert_alpha()
        self.main_menu_img = load('assets/buttons/MainMenu.png').convert_alpha()
        self.title_img = load('assets/buttons/Title.png').convert_alpha()
        self.resume_img = load('assets/buttons/Resume.png').convert_alpha()
        self.pause_img = load('assets/buttons/Pause.png').convert_alpha()
        self.exit_img = load('assets/buttons/Exit.png').convert_alpha()
        self.bg_img = load('assets/bg and cursor/Background.png').convert_alpha()
        self.bg_playing_img = load('assets/bg and cursor/Background_Playing.jpg').convert_alpha()
        self.bg_paused_img = load('assets/bg and cursor/Background_Pause.jpg').convert_alpha()
        self.battle_field_imd = load('assets/bg and cursor/Battle_Field.png').convert_alpha()
        self.audio_off_img = load('assets/buttons/button_slider_animation/button_17.png').convert_alpha()
        self.audio_on_img = load('assets/buttons/button_slider_animation/button_1.png').convert_alpha()
        self.male_img = load('assets/buttons/boy.png').convert_alpha()
        self.female_img = load('assets/buttons/girl.png').convert_alpha()


        self.jumping_sound = pygame.mixer.Sound('assets/sounds/player/boy/jump/jumping.wav')
        self.walking = pygame.mixer.Sound('assets/sounds/player/boy/walk/sfx_step_grass_l.flac')

        self.play_button = button.Button(((self.screen.get_width() / 2) - (self.play_img.get_width() / 2) * 3), 290, self.play_img, 3.0)
        self.settings_button = button.Button(((self.screen.get_width() / 2) - (self.settings_img.get_width() / 2) * 3), 390, self.settings_img, 3.0)
        self.quit_button = button.Button(((self.screen.get_width() / 2) - (self.quit_img.get_width() / 2) * 3), 490, self.quit_img, 3.0)
        self.exit_button = button.Button(((self.screen.get_width() / 2) - (self.exit_img.get_width() / 2) * 3), 490, self.exit_img, 3.0)
        self.audio_button = button.Button(((self.screen.get_width() / 2) - (self.audio_img.get_width() / 2) * 3), 110, self.audio_img, 3.0)
        self.audio_on_button = button.Button(((self.screen.get_width() / 2) - (self.audio_on_img.get_width() / 2) * 3), 210, self.audio_on_img, 3.0)
        self.audio_off_button = button.Button(((self.screen.get_width() / 2) - (self.audio_off_img.get_width() / 2) * 3), 210, self.audio_off_img, 3.0)
        self.back_button = button.Button(((self.screen.get_width() / 2) - (self.back_img.get_width() / 2) * 3), 470, self.back_img, 3)
        self.main_menu_button = button.Button(((self.screen.get_width() / 2) - (self.main_menu_img.get_width() / 2) * 3.5), 20, self.main_menu_img, 3.5)
        self.title_button = button.Button(((self.screen.get_width() / 2) - (self.title_img.get_width() / 2) * 3.5), 20, self.title_img, 3.5)
        self.resume_button = button.Button(((self.screen.get_width() / 2) - (self.resume_img.get_width() / 2) * 3), 290, self.resume_img, 3.0)
        self.pause_button = button.Button(1205, 5, self.pause_img, 1.5)

        self.male_button = button.Button(100, ((self.screen.get_height() / 2) - (self.male_img.get_height() / 2) * 0.8), self.male_img, 0.8)
        self.female_button = button.Button(900, ((self.screen.get_height() / 2) - (self.male_img.get_height() / 2) * 0.8), self.female_img, 0.8)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.moving_left = True
                if event.key == pygame.K_RIGHT:
                    self.player.moving_right = True
                if event.key == pygame.K_a:
                    self.player.moving_left = True
                if event.key == pygame.K_d:
                    self.player.moving_right = True
                if not self.player.jump and not self.player.in_air:
                    if event.key == pygame.K_SPACE and self.player.alive:
                        self.player.jump = True
                        self.player.in_air = True
                        self.player.play_sound += 1
                        if not self.muted and self.player.jump:
                            if self.player.play_sound == 1:
                                self.jumping_sound.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.moving_left = False
                if event.key == pygame.K_RIGHT:
                    self.player.moving_right = False
                if event.key == pygame.K_a:
                    self.player.moving_left = False
                if event.key == pygame.K_d:
                    self.player.moving_right = False

    def run(self):
        keys = pygame.key.get_pressed()

        if self.playing:
            self.screen.blit(self.bg_paused_img, (0, 0))
        else:
            self.screen.blit(self.bg_img, (0, 0))

        if self.game_paused:
            if self.menu_state == "main":
                self.title_button.status()

                if self.play_button.draw():
                    time.sleep(0.3)
                    self.playing = True
                    self.game_paused = False
                    self.menu_state = 'playing'

                if self.settings_button.draw():
                    self.menu_state = "settings"

                if self.exit_button.draw():
                    pygame.quit()
                    sys.exit()

            if self.menu_state == "playing":
                self.main_menu_button.status()

                if self.resume_button.draw():
                    self.game_paused = False

                if self.settings_button.draw():
                    self.menu_state = "settings"

                if self.quit_button.draw():
                    self.playing = False
                    self.has_gender = False
                    self.game_paused = True
                    self.menu_state = 'main'

            if self.menu_state == "settings":

                if self.muted:
                    self.audio_off_button.status()

                if not self.muted:
                    self.audio_on_button.status()

                if self.audio_button.draw():
                    if not self.muted:
                        self.muted = True

                    elif self.muted:
                        self.muted = False

                if self.back_button.draw():
                    if self.playing:
                        self.menu_state = 'playing'

                    else:
                        self.menu_state = 'main'

                if keys[pygame.K_ESCAPE]:

                    if self.playing and self.click == 0:
                        self.click = 1
                        time.sleep(0.3)
                        self.menu_state = 'playing'

                    elif self.playing and self.click == 1:
                        self.click = 0
                        time.sleep(0.3)
                        self.game_paused = False

                    else:
                        time.sleep(0.3)
                        self.menu_state = 'main'

        if not self.game_paused and self.playing:

            if self.male_button.draw():
                self.gender = 'boy'
                self.has_gender = True
                self.player = Player('player', self.gender, 250, 520, 0.15, 3)
            if self.female_button.draw():
                self.gender = 'girl'
                self.has_gender = True
                self.player = Player('player', self.gender, 250, 520, 0.15, 3)
            if self.has_gender:
                if self.game_status == "battle":
                    self.screen.blit(self.battle_field_imd, (0, 0))

                else:
                    self.screen.blit(self.bg_playing_img, (0, 0))
                    self.health.draw(self.player.health)
                    self.world.draw()
                    self.player.run()

                if self.pause_button.draw():
                    self.game_paused = True

                if keys[pygame.K_ESCAPE]:
                    self.game_paused = True
                    time.sleep(0.2)

            if self.player.alive:
                if self.player.in_air:
                    self.player.update_action(2)
                elif self.player.moving_left or self.player.moving_right:
                    self.player.update_action(1)
                else:
                    self.player.update_action(0)
                self.world.screen_scroll = self.player.move(self.player.moving_left, self.player.moving_right)
            if self.player.game_over == 1:
                self.player = Player('player', self.gender, 250, 520, 0.15, 3)
                self.world.screen_scroll = 0
                self.player.screen_scroll = 0

            if self.player.rect.top >= self.screen.get_height():
                self.player.game_over = 1

        self.event_loop()
