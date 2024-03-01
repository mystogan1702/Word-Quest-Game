from settings import *
from world import World


class Player(pygame.sprite.Sprite):

    def __init__(self, char_type, gender, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.play_sound = 0
        self.moving_left = False
        self.moving_right = False
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.world = World(world_data)
        animation_types = ["idle", "walking", "jumping"]
        for animation in animation_types:
            temp_list = []

            num_of_frames = len(os.listdir(f'assets/{self.char_type}/{gender}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'assets/{self.char_type}/{gender}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
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

        if self.jump and not self.in_air:
            self.vel_y = -15
            self.jump = False
            self.play_sound = 0
            self.in_air = True

        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        for tile in self.world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom + self.surface.get_height():
            self.rect.bottom - self.surface.get_height()
            dy = 0

    def update_animation(self):
        animation_cd = 100

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        pygame.draw.rect(self.surface, (255, 255, 255), self.rect, 2)
        self.surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


    def run(self):
        self.update_animation()
        self.draw()

        if self.alive:
            if self.in_air:
                self.update_action(2)
            elif self.moving_left or self.moving_right:
                self.update_action(1)
            else:
                self.update_action(0)
            self.move(self.moving_left, self.moving_right)
