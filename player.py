from settings import *
from world import World


class Player(pygame.sprite.Sprite):

    def __init__(self, char_type, gender, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.health = 10
        self.max_health = 10
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
        self.game_over = 0
        animation_types = ["idle", "walking", "jumping"]
        for animation in animation_types:
            temp_list = []

            num_of_frames = len(os.listdir(f'assets/{self.char_type}/{gender}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'assets/{self.char_type}/{gender}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.player = self.animation_list[self.action][self.frame_index]
        self.rect = self.player.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.player.get_width()
        self.height = self.player.get_height()
        self.surface = pygame.display.get_surface()
        self.surface_width = self.surface.get_width()
        self.surface_height = self.surface.get_height()

    def run(self):
        self.update_animation()
        self.draw()

    def move(self, moving_left, moving_right):
        self.screen_scroll = 0

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
            self.vel_y = -17
            self.jump = False
            self.play_sound = 0
            self.in_air = True

        self.vel_y += gravity
        if self.vel_y > 15:
            self.vel_y
        dy += self.vel_y

        for tile in self.world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom


        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > self.surface_width:
                dx = 0

        self.rect.x += dx
        self.rect.y += dy

        #if self.char_type == 'player':
        #    if self.rect.right > self.surface_width - scroll_thresh or self.rect.left < scroll_thresh:
        #        self.rect.x -= dx
        #        self.screen_scroll = -dx

        #return self.screen_scroll

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
        self.surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


