import pygame

from game import *
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from settings import *


class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.origin = vector()
        self.pan_active = False
        self.pan_offset = vector()

        self.support_line_surf = pygame.Surface(windowSize)
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(10)

    def event_loop(self):
        self.pan_input(event)

    def pan_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_active = True
            self.pan_offset = vector(mouse_pos()) - self.origin

        if not mouse_buttons()[1]:
            self.pan_active = False

        if event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y * 50
            else:
                self.origin.x -= event.y * 50

        if self.pan_active:
            self.origin = vector(mouse_pos()) - self.pan_offset

    def draw_tile_lines(self):
        cols = window_width // tile_size
        rows = window_height // tile_size

        origin_offset = vector(
            x=self.origin.x - int(self.origin.x / tile_size) * tile_size,
            y=self.origin.y - int(self.origin.y / tile_size) * tile_size)

        self.support_line_surf.fill('green')

        for col in range(cols + 1):
            x = origin_offset.x + col * tile_size
            pygame.draw.line(self.support_line_surf, Line_Color, (x,0), (x,window_height))

        for row in range(rows + 1):
            y = origin_offset.y + row * tile_size
            pygame.draw.line(self.support_line_surf, Line_Color, (0, y), (window_width, y))

        self.display_surface.blit(self.support_line_surf, (0, 0))

    def run(self, fps):
        self.event_loop()

        self.display_surface.fill('white')
        self.draw_tile_lines()
        pygame.draw.circle(self.display_surface, 'red', self.origin, 10)


