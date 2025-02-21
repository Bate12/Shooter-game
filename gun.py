import pygame
from settings import *

class Gun():
    def __init__(self):
        self.pos = pygame.Vector2()
        self.size = 15
        self.halfSize = self.size // 2
        self.color = (0,0,0)
        self.bullColor = (0,150,150)
        self.rect = pygame.Rect(self.pos.x ,self.pos.y, self.size, self.size)

        self.image = pygame.image.load('assets/gun.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.angle = 0

        self.shootVel = 0.8
        self.bullets = []

        self.shootSFX = pygame.mixer.Sound("assets/laserShoot.wav")

    def updateRect(self):
        self.rect = pygame.Rect(self.pos.x ,self.pos.y, self.size, self.size)

    def shoot(self, dir):
        bullInitPos = self.pos.copy()
        self.bullets.append([bullInitPos, pygame.Rect(bullInitPos.x ,bullInitPos.y, 10, 10) , dir])
        pygame.mixer.Sound.play(self.shootSFX).set_volume(VOLUME)

    def rotateTo(self, dir):
        self.angle = dir.angle_to(pygame.Vector2(1,0))

    def update(self, player):
        self.pos = pygame.Vector2(player.pos.x, player.pos.y)
        

        self.updateRect()

    def render(self, win):
        #pygame.draw.rect(win, self.color, self.rect)
        rotatedImage = self.image.copy()
        if self.angle > 90 or self.angle < -90:
            rotatedImage = pygame.transform.flip(rotatedImage, False, True)
        rotatedImage = pygame.transform.rotozoom(rotatedImage, self.angle, 1)
        win.blit(rotatedImage, self.rect)
        

if __name__ == "__main__":
    quit()
