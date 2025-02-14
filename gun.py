import pygame
from settings import *

class Gun():
    def __init__(self):
        self.pos = pygame.Vector2()
        self.size = 15
        self.color = (0,0,0)
        self.bullColor = (0,150,150)
        self.rect = pygame.Rect(self.pos.x ,self.pos.y, self.size, self.size)

        self.shootVel = 1
        self.bullets = []

        self.shootSFX = pygame.mixer.Sound("assets/laserShoot.wav")

    def updateRect(self):
        self.rect = pygame.Rect(self.pos.x ,self.pos.y, self.size, self.size)

    def shoot(self, dir):
        bullInitPos = self.pos.copy()
        self.bullets.append([bullInitPos, pygame.Rect(bullInitPos.x ,bullInitPos.y, 10, 10) , dir])
        pygame.mixer.Sound.play(self.shootSFX).set_volume(VOLUME)

    def update(self, player):
        self.pos = pygame.Vector2(player.pos.x, player.pos.y)
        

        self.updateRect()

    def render(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        

if __name__ == "__main__":
    quit()
