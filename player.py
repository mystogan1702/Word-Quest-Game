import pygame.display

from settings import *

class Player:
    def __init__(self):
        self.character_img = pygame.image.load('assets/player/character_looking_right.png').convert_alpha()
        width = self.character_img.get_width()
        height = self.character_img.get_height()
        self.character = pygame.transform.scale(self.character_img, (int(width * 0.05), int(height * 0.05)))
        self.surface = pygame.display.get_surface()

    def draw(self):
        self.surface.blit(self.character, (0, 0))