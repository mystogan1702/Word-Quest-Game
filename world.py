import pygame

from settings import *

class World():
    def __init__(self, data):
        self.tile_list = []
        self.screen = pygame.display.get_surface()

        grass_img = pygame.image.load('assets/blocks/grass_block.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            self.screen.blit(tile[0], tile[1])
            pygame.draw.rect(self.screen, (255,255,255), tile[1], 1)