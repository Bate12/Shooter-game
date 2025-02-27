import pygame, math
from object import Object
from settings import *

class Enemy(Object):
    def __init__(self, game, pos, size, speed, color=(200,50,50)):
        super().__init__(game, pos, size, speed=speed, color=color ,isCentered=False)

    def update(self):
        self.moveTowards(self.game.player.pos)

        self.updateRect()


if __name__ == "__main__":
    quit()
