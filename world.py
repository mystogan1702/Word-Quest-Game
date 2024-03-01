import pygame

from settings import *

class World(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.platform_img = pygame.image.load('assets/player/boy/idle/player_idle[0].png')
        self.image.blit(self.platform_img, (0, 0))
        self.rect = self.image.get_rect(topleft = pos)