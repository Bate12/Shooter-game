import pygame, math
from settings import *

class Projectile:
    def __init__(self, pos, direction, speed=5, size=5, color=(255, 0, 0), friendly=True):
        self.pos = pygame.Vector2(pos)
        self.direction = direction.normalize()
        self.speed = speed
        self.size = size
        self.color = color
        self.friendly = friendly  # True = přátelský, False = nepřátelský
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
    
    def update(self):
        self.pos += self.direction * self.speed
        self.rect.topleft = self.pos
    
    def render(self, win):
        pygame.draw.rect(win, self.color, self.rect)

if __name__ == "__main__":
    quit()