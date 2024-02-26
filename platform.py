import pygame

from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.platform_img = pygame.image.load('assets/player/character_looking_right.png')
        self.image.blit(self.platform_img, (0, 0))
        self.rect = self.image.get_rect(topleft = pos)