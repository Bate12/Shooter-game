import pygame as pg
from pygame.math import Vector2 as Vec
import math
from settings import *

class Object(pg.sprite.Sprite):
    def __init__(self, game, pos, width, height = None, speed = 1, color = (0,255,0), isCentered = True):
        super().__init__()

        self.width = width
        if height == None:
            self.height = self.width
        else:
            self.height = height
        self.halfWidth = self.width//2
        self.halfHeight = self.height//2

        self.color = color
        self.image = pg.Surface([self.width, self.height]) 
        self.image.fill((255,255,255)) 
        self.image.set_colorkey(self.color)

        self.pos = Vec(pos)
        self.vel = speed

        self.rect = self.image.get_rect()
        self.isCentered = isCentered

        self.game = game

        self.updateRect()

    def updateRect(self):
        if self.isCentered:
            self.rect.center = self.pos
        else:
            self.rect.topleft = self.pos

    def moveTowards(self, target: Vec | list | tuple):
        if isinstance(target, list | tuple):
            target = Vec(target[0], target[1])
        self.pos = self.pos.move_towards(target, self.vel)
        self.updateRect()

    def update(self):
        super().__init__()

        #self.moveTowards(self.game.player.pos)

        


if __name__ == "__main__":
    quit()
