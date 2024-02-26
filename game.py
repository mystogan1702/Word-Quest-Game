import pygame.transform

import button

from pygame.image import load
from settings import *
from level import Level
from player import Player


class Game:
    def __init__(self):
        self.game_paused = True
        self.playing = False
        self.menu_state = "main"
        self.muted = False
        self.current_stage = Level()
        self.screen = pygame.display.set_mode(windowSize)
        self.click = 0
        self.click_paused = 0
        self.movement = [False, False]
        self.game_status = "adventure"
        self.player = Player()

        surf = load('assets/others/Cursor.png').convert_alpha()
        width = surf.get_width()
        height = surf.get_height()
        cursor_img = pygame.transform.scale(surf, (int(width * 0.5), int(height * 0.5)))
        cursor = pygame.cursors.Cursor((0, 0), cursor_img)
        pygame.mouse.set_cursor(cursor)

        self.play_img = pygame.image.load('assets/buttons/play.png').convert_alpha()
        self.quit_img = pygame.image.load('assets/buttons/Quit.png').convert_alpha()
        self.settings_img = pygame.image.load('assets/buttons/Settings.png').convert_alpha()
        self.back_img = pygame.image.load('assets/buttons/Back.png').convert_alpha()
        self.audio_img = pygame.image.load('assets/buttons/Audio.png').convert_alpha()
        self.audio_on_img = pygame.image.load('assets/buttons/Audio_On.png').convert_alpha()
        self.audio_off_img = pygame.image.load('assets/buttons/Audio_Off.png').convert_alpha()
        self.main_menu_img = pygame.image.load('assets/buttons/MainMenu.png').convert_alpha()
        self.title_img = pygame.image.load('assets/buttons/Title.png').convert_alpha()
        self.resume_img = pygame.image.load('assets/buttons/Resume.png').convert_alpha()
        self.pause_img = pygame.image.load('assets/buttons/Pause.png').convert_alpha()
        self.exit_img = pygame.image.load('assets/buttons/Exit.png').convert_alpha()

        self.bg_img = pygame.image.load('assets/others/Background.jpg').convert_alpha()
        self.bg_playing_img = pygame.image.load('assets/others/Background_Playing.jpg').convert_alpha()
        self.bg_paused_img = pygame.image.load('assets/others/Background_Pause.jpg').convert_alpha()
        self.battle_field_imd = pygame.image.load('assets/others/Battle_Field.png').convert_alpha()


        self.play_button = button.Button(540, 290, self.play_img, 3.0)
        self.settings_button = button.Button(460, 390, self.settings_img, 3.0)
        self.quit_button = button.Button(540, 490, self.quit_img, 3.0)
        self.exit_button = button.Button(540, 490, self.exit_img, 3.0)
        self.audio_button = button.Button(540, 110, self.audio_img, 0.8)
        self.audio_on_button = button.Button(540, 190, self.audio_on_img, 0.8)
        self.audio_off_button = button.Button(540, 190, self.audio_off_img, 0.8)
        self.back_button = button.Button(540, 470, self.back_img, 0.8)
        self.main_menu_button = button.Button(400, 20, self.main_menu_img, 3.5)
        self.title_button = button.Button(370, 20, self.title_img, 3.5)
        self.resume_button = button.Button(500, 290, self.resume_img, 3.0)
        self.pause_button = button.Button(5, 5, self.pause_img, 1.5)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
            if self.game_status == "battle":
                self.screen.blit(self.battle_field_imd, (0, 0))

            else:
                self.screen.blit(self.bg_playing_img, (0, 0))
                self.player.draw()

            if self.pause_button.draw():
                self.game_paused = True

            if keys[pygame.K_ESCAPE]:
                self.game_paused = True
                time.sleep(0.2)