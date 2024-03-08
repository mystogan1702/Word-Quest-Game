import pygame
from pygame import mixer
import os
import random
import csv
import button
import time
import sys

mixer.init()
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Word Quest')

clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 18
MAX_LEVELS = 3
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False

playing = False
menu_state = 'main'
game_paused = True
has_gender = False
muted = False
click = 0
game_status = "adventure"
gender = 'boy'
jump_sound = 0
current_seconds = 3
time_remaining = 300
game_complete = False
pygame.time.set_timer(pygame.USEREVENT, 1000)

moving_left = False
moving_right = False

pygame.mixer.music.load('assets/audio/music2.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('assets/audio/jump.wav')
jump_fx.set_volume(0.05)

surf = pygame.image.load('assets/img/cursor/Cursor.png').convert_alpha()
width = surf.get_width()
height = surf.get_height()
cursor_img = pygame.transform.scale(surf, (int(width * 0.5), int(height * 0.5)))
cursor = pygame.cursors.Cursor((0, 0), cursor_img)
pygame.mouse.set_cursor(cursor)

play_img = pygame.image.load('assets/img/buttons/play.png').convert_alpha()
quit_img = pygame.image.load('assets/img/buttons/Quit.png').convert_alpha()
settings_img = pygame.image.load('assets/img/buttons/Settings.png').convert_alpha()
back_img = pygame.image.load('assets/img/buttons/Back.png').convert_alpha()
audio_img = pygame.image.load('assets/img/buttons/Audio.png').convert_alpha()
main_menu_img = pygame.image.load('assets/img/buttons/MainMenu.png').convert_alpha()
title_img = pygame.image.load('assets/img/buttons/Title.png').convert_alpha()
resume_img = pygame.image.load('assets/img/buttons/Resume.png').convert_alpha()
pause_img = pygame.image.load('assets/img/buttons/Pause.png').convert_alpha()
exit_img = pygame.image.load('assets/img/buttons/Exit.png').convert_alpha()
bg_img = pygame.image.load('assets/img/bg and cursor/Background.png').convert_alpha()
bg_playing_img = pygame.image.load('assets/img/bg and cursor/Background_Playing.jpg').convert_alpha()
bg_paused_img = pygame.image.load('assets/img/bg and cursor/Background.png').convert_alpha()
battle_field_imd = pygame.image.load('assets/img/bg and cursor/Battle_Field.png').convert_alpha()
audio_off_img = pygame.image.load('assets/img/buttons/button_slider_animation/button_17.png').convert_alpha()
audio_on_img = pygame.image.load('assets/img/buttons/button_slider_animation/button_1.png').convert_alpha()
male_img = pygame.image.load('assets/img/buttons/boy.png').convert_alpha()
female_img = pygame.image.load('assets/img/buttons/girl.png').convert_alpha()

img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'assets/img/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)

font = pygame.font.SysFont('Futura', 30)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_level():
    enemy_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    # create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, gender, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0
        self.vulnerable = True
        self.player_idling = False
        self.counter = current_seconds
        self.can_move = True

        if char_type == 'player':
            animation_types = ['idle', 'walking', 'jumping']
            for animation in animation_types:
                temp_list = []
                num_of_frames = len(os.listdir(f'assets/img/{self.char_type}/{gender}/{animation}'))
                for i in range(num_of_frames):
                    img = pygame.image.load(f'assets/img/{self.char_type}/{gender}/{animation}/{i}.png').convert_alpha()
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
                self.animation_list.append(temp_list)
        if char_type == 'enemy':
            animation_types = ['walking', 'walking', 'walking']
            for animation in animation_types:
                temp_list = []
                num_of_frames = len(os.listdir(f'assets/img/{self.char_type}/{gender}/{animation}'))
                for i in range(num_of_frames):
                    img = pygame.image.load(f'assets/img/{self.char_type}/{gender}/{animation}/{i}.png').convert_alpha()
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
                self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()

    def move(self, moving_left, moving_right):
        screen_scroll = 0
        dx = 0
        dy = 0

        if self.can_move:
            if moving_left:
                dx = -self.speed
                self.flip = True
                self.direction = -1
            if moving_right:
                dx = self.speed
                self.flip = False
                self.direction = 1

            if self.jump and not self.in_air:
                self.vel_y = -13
                self.jump = False
                self.in_air = True

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        if self.vulnerable:
            if self.char_type == 'player':
                if pygame.sprite.spritecollide(self, enemy_group, False):
                    self.health -= 5
                    self.vulnerable = False
                    self.can_move = False
                    if moving_left:
                        dx = 30
                        dy = -30
                        self.flip = False
                        self.direction = 1
                    elif moving_right:
                        dx = -30
                        dy = -30
                        self.flip = False
                        self.direction = -1
                    elif self.player_idling and player.direction == 1:
                        dx = -30
                        dy = -30
                        self.flip = False
                        self.direction = 1
                    elif self.player_idling and player.direction == -1:
                        dx = 30
                        dy = -30
                        self.flip = False
                        self.direction = -1

        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        self.rect.x += dx
        self.rect.y += dy

        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll <
                    (world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                    or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(0)
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        # scroll
        self.rect.x += screen_scroll

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(2)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 2:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 3 and tile <= 4:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 5 and tile <= 11:
                        decoration_1 = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration_1)
                    elif tile == 12:
                        player = Player('player', gender, x * TILE_SIZE, y * TILE_SIZE, 0.1, 4)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 13:
                        enemy_1 = Player('enemy', 'mosquito', x * TILE_SIZE, y * TILE_SIZE, 0.09, 2)
                        enemy_group.add(enemy_1)
                    elif tile == 14:
                        enemy_2 = Player('enemy', 'bee', x * TILE_SIZE, y * TILE_SIZE, 0.07, 2)
                        enemy_group.add(enemy_2)
                    elif tile == 15:
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    elif tile >= 16 and tile <= 17:
                        self.obstacle_list.append(tile_data)

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour,
                             (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour,
                             (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction == 2:
            pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        return fade_complete

intro_fade = ScreenFade(1, BLACK, 10)
death_fade = ScreenFade(2, PINK, 10)

play_button = button.Button(((screen.get_width() / 2) - (play_img.get_width() / 2) * 3), 290,
                            play_img, 3.0)
settings_button = button.Button(((screen.get_width() / 2) - (settings_img.get_width() / 2) * 3), 390,
                                settings_img, 3.0)
quit_button = button.Button(((screen.get_width() / 2) - (quit_img.get_width() / 2) * 3), 490,
                            quit_img, 3.0)
exit_button = button.Button(((screen.get_width() / 2) - (exit_img.get_width() / 2) * 3), 490,
                            exit_img, 3.0)
audio_button = button.Button(((screen.get_width() / 2) - (audio_img.get_width() / 2) * 3), 110,
                             audio_img, 3.0)
audio_on_button = button.Button(((screen.get_width() / 2) - (audio_on_img.get_width() / 2) * 3), 210,
                                audio_on_img, 3.0)
audio_off_button = button.Button(((screen.get_width() / 2) - (audio_off_img.get_width() / 2) * 3), 210,
                                 audio_off_img, 3.0)
back_button = button.Button(((screen.get_width() / 2) - (back_img.get_width() / 2) * 3), 470,
                            back_img, 3)
main_menu_button = button.Button(((screen.get_width() / 2) - (main_menu_img.get_width() / 2) * 3.5), 20,
                                 main_menu_img, 3.5)
title_button = button.Button(((screen.get_width() / 2) - (title_img.get_width() / 2) * 3.5), 20,
                             title_img, 3.5)
resume_button = button.Button(((screen.get_width() / 2) - (resume_img.get_width() / 2) * 3), 290,
                              resume_img, 3.0)
pause_button = button.Button(1205, 5, pause_img, 1.5)

male_button = button.Button(100, ((screen.get_height() / 2) - (male_img.get_height() / 2) * 0.8), male_img, 0.8)
female_button = button.Button(900, ((screen.get_height() / 2) - (male_img.get_height() / 2) * 0.8), female_img, 0.8)

enemy_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
with open(f'assets/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data)

while True:
    clock.tick(FPS)

    keys = pygame.key.get_pressed()

    if playing:
        screen.blit(bg_paused_img, (0, 0))
    else:
        screen.blit(bg_img, (0, 0))

    if game_paused:
        if menu_state == "main":
            title_button.status(screen)

            if play_button.draw(screen):
                time.sleep(0.3)
                playing = True
                game_paused = False
                menu_state = 'playing'

            if settings_button.draw(screen):
                menu_state = "settings"

            if exit_button.draw(screen):
                pygame.quit()
                sys.exit()

        if menu_state == "playing":
            main_menu_button.status(screen)

            if resume_button.draw(screen):
                game_paused = False

            if settings_button.draw(screen):
                menu_state = "settings"

            if quit_button.draw(screen):
                time.sleep(0.3)
                game_paused = True
                menu_state = "main"
                playing = False
                has_gender = False

        if menu_state == "settings":

            if muted:
                audio_off_button.status(screen)

            if not muted:
                audio_on_button.status(screen)

            if audio_button.draw(screen):
                if not muted:
                    muted = True
                    pygame.mixer_music.pause()

                elif muted:
                    muted = False
                    pygame.mixer_music.unpause()

            if back_button.draw(screen):
                if playing:
                    time.sleep(0.3)
                    menu_state = 'playing'

                else:
                    time.sleep(0.3)
                    menu_state = 'main'

            if keys[pygame.K_ESCAPE]:

                if playing and click == 0:
                    click = 1
                    time.sleep(0.3)
                    menu_state = 'playing'

                elif playing and click == 1:
                    click = 0
                    time.sleep(0.3)
                    game_paused = False

                else:
                    time.sleep(0.3)
                    menu_state = 'main'

    if not game_paused and playing:
        if not game_complete:
            if not has_gender:
                if male_button.draw(screen):
                    gender = 'boy'
                    has_gender = True
                    player = Player('player', gender, x * TILE_SIZE, y * TILE_SIZE, 0.1, 4)
                if female_button.draw(screen):
                    gender = 'girl'
                    has_gender = True
                    player = Player('player', gender, x * TILE_SIZE, y * TILE_SIZE, 0.1, 4)
            if has_gender:
                if game_status == "battle":
                    screen.blit(battle_field_imd, (0, 0))

                else:
                    screen.blit(bg_playing_img, (0, 0))
                    world.draw()
                    health_bar.draw(player.health)

                    player.update()
                    player.draw()

                    for enemy in enemy_group:
                        enemy.ai()
                        enemy.update()
                        enemy.draw()

                    decoration_group.update()
                    water_group.update()
                    exit_group.update()
                    decoration_group.draw(screen)
                    water_group.draw(screen)
                    exit_group.draw(screen)

                    if start_intro == True:
                        if intro_fade.fade():
                            start_intro = False
                            intro_fade.fade_counter = 0

                    if player.alive:
                        if player.in_air:
                            player.update_action(2)
                        elif moving_left or moving_right:
                            player.update_action(1)
                        else:
                            player.update_action(0)
                            player.player_idling = True
                        screen_scroll, level_complete = player.move(moving_left, moving_right)
                        bg_scroll -= screen_scroll
                        if level_complete:
                            start_intro = True
                            level += 1
                            bg_scroll = 0
                            world_data = reset_level()
                            if level <= MAX_LEVELS:
                                with open(f'assets/level{level}_data.csv', newline='') as csvfile:
                                    reader = csv.reader(csvfile, delimiter=',')
                                    for x, row in enumerate(reader):
                                        for y, tile in enumerate(row):
                                            world_data[x][y] = int(tile)
                                world = World()
                                player, health_bar = world.process_data(world_data)
                        if level == 4:
                            game_complete = True

                    else:
                        screen_scroll = 0
                        if death_fade.fade():
                            if not player.alive:
                                death_fade.fade_counter = 0
                                start_intro = True
                                bg_scroll = 0
                                world_data = reset_level()
                                with open(f'assets/level{level}_data.csv', newline='') as csvfile:
                                    reader = csv.reader(csvfile, delimiter=',')
                                    for x, row in enumerate(reader):
                                        for y, tile in enumerate(row):
                                            world_data[x][y] = int(tile)
                                world = World()
                                player, health_bar = world.process_data(world_data)

                if pause_button.draw(screen):
                    game_paused = True

                if keys[pygame.K_ESCAPE]:
                    game_paused = True
                    time.sleep(0.2)
                if level == 3:
                    draw_text(f'The Game will Stop in {time_remaining} seconds...', font, BLACK, ((SCREEN_WIDTH / 2) - 100), 20)
                    if time_remaining == 0:
                        game_complete = True
        else:
            game_paused = True
            playing = False
            menu_state = "main"
            has_gender = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if level == 3:
            if event.type == pygame.USEREVENT:
                time_remaining -= 1
                print(time_remaining)
        if not player.vulnerable:
            player.update_action(0)
            if event.type == pygame.USEREVENT:
                current_seconds -= 1
            if current_seconds == 2:
                player.can_move = True
            if current_seconds == 0:
                player.vulnerable = True
                current_seconds = 3
        if player.can_move:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if not player.jump and not player.in_air:
                    if event.key == pygame.K_SPACE and player.alive:
                        player.jump = True
                        player.in_air = True
                        jump_sound = 1
                        if not muted and player.jump:
                            if jump_sound == 1:
                                jump_fx.play()
                    if event.key == pygame.K_w and player.alive:
                        player.jump = True
                        player.in_air = True
                        jump_sound = 1
                        if not muted and player.jump:
                            if jump_sound == 1:
                                jump_fx.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()