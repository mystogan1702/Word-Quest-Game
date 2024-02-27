import pygame

from settings import *
class Player:
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.character_img = pygame.image.load('assets/player/character_looking_right.png').convert_alpha()
        width = self.character_img.get_width()
        height = self.character_img.get_height()
        self.character = pygame.transform.scale(self.character_img, (150, 150))
        self.player_x = 300
        self.player_y = 500
        self.player_direction_x = 0
        self.player_direction_y = 0
        self.player_speed = 3

    def draw(self):
        self.surface.blit(self.character, (0, 500))
