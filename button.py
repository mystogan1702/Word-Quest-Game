import pygame, time


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click = False
        self.surface = pygame.display.get_surface()

    def status(self):
        self.surface.blit(self.image, (self.rect.x, self.rect.y))

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if not self.click:
                if pygame.mouse.get_pressed()[0] == 1:
                    self.click = True
                    time.sleep(0.2)
                    action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.click = False

        self.surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

