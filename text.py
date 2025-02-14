import pygame
from pygame.locals import *
from pygame.math import Vector2 as Vec

class Text:
    def __init__(self, text, x, y, font_size=30, font_color=(0,0,0)):
        pygame.init()

        self.Pos = Vec(x, y)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.isVisable = True
        
        self.font = pygame.font.SysFont('Comic Sans MS', self.font_size)
        self.surface = self.font.render(self.text, True, self.font_color)
        self.rect = self.surface.get_rect(center=self.Pos)

    def update(self, new_text):
        self.text = new_text
        self.surface = self.font.render(self.text, True, self.font_color)

    def render(self, win):
        if self.isVisable:
            win.blit(self.surface, self.rect)