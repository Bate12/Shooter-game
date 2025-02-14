import pygame, math
from settings import *

class Enemy():
    def __init__(self, pos, size, speed):
        self.pos = pygame.Vector2(pos)
        self.vel = speed
        self.size = size
        self.color = (200,50,50)
        self.rect = pygame.Rect(self.pos.x ,self.pos.y, self.size, self.size)

    def updateRect(self):
        self.rect = pygame.Rect(self.pos.x ,self.pos.y, self.size, self.size)

    def update(self, player):
        self.pos = self.pos.move_towards(player.pos, self.vel)

        self.updateRect()

    def render(self, win):
        pygame.draw.rect(win, self.color, self.rect)

if __name__ == "__main__":
    quit()
