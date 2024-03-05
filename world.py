from settings import *


class World:
    def __init__(self, data):
        self.tile_list = []
        self.screen = pygame.display.get_surface()
        self.screen_scroll = -1

        grass_img = pygame.image.load('assets/blocks/grass_block.png').convert_alpha()
        dirt_img = pygame.image.load('assets/blocks/dirt_block.jpg').convert_alpha()

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
                elif tile == 2:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            tile[1][0] += self.screen_scroll
            self.screen.blit(tile[0], tile[1])
