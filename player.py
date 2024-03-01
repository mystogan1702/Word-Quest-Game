from settings import *


class Player(pygame.sprite.Sprite):

    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(4):
            img = pygame.image.load(f'assets/player/{char_type}/idle/player_idle[{i}].png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.surface = pygame.display.get_surface()

    def move(self, moving_left, moving_right):

        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        animation_cd = 100

        self.image = self.animation_list[self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0


    def draw(self):
        self.surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
