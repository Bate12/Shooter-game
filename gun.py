import pygame as pg
from pygame.math import Vector2 as Vec
from settings import *

class Gun(pg.sprite.Sprite):
    def __init__(self, game, player):
        super().__init__()

        self.game = game
        self.player = player

        self.size = 15
        self.halfSize = self.size // 2
        self.color = (0, 0, 0)
        self.bullColor = (0, 150, 150)

        # Load and transform the image
        self.image = pg.image.load('assets/gun.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (self.size, self.size))
        self.orig_image = self.image  # Keep the original for rotation
        
        self.rect = self.image.get_rect()
        self.pos = Vec(self.player.pos.x, self.player.pos.y)
        
        self.angle = 0
        self.shootVel = 0.6
        self.bullets = []
        self.distance = 25

        self.shootSFX = pg.mixer.Sound("assets/laserShoot.wav")

    def updateRect(self):
        self.rect.center = self.pos

    def shoot(self, dir):
        bullInitPos = self.pos.copy()
        self.bullets.append([bullInitPos, pg.Rect(bullInitPos.x, bullInitPos.y, 10, 10), dir])
        
        pg.mixer.Sound.play(self.shootSFX).set_volume(VOLUME)

    def rotateTo(self, dir):
        self.angle = dir.angle_to(Vec(1, 0))
        self.image = pg.transform.rotate(self.orig_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def getClosest(self, objectList):
        closestMag = 1000
        closestObj = None
        if len(objectList) == 0:
            self.closest = None
            return None

        for obj in objectList:
            distance = obj.pos - self.player.pos
            distance = distance.length()
            if not closestObj or closestMag > distance:
                closestMag = distance
                closestObj = obj
            
        if closestObj == None:
            return None
        
        closestObj.pos + (GENERAL_SIZE//2, GENERAL_SIZE//2)
        return closestObj

    def update(self):
        # Update position to follow the player
        

        # Rotate towards the mouse
        self.target = self.getClosest(self.game.enemies)
        try:
            self.closest = self.target.pos
            direction = Vec(self.closest - self.player.pos)
            self.rotateTo(direction)

            direction.normalize_ip()
            self.pos = self.player.pos + (direction * self.distance, direction * self.distance)
        except:
            pass

        # Update the rectangle for positioning
        self.updateRect()

        # Update bullets
        for bullet in self.bullets:
            bullet[0] += bullet[2] * self.shootVel
            bullet[1].center = bullet[0]

            # Remove bullets that are off-screen
            if not self.game.win.get_rect().colliderect(bullet[1]):
                self.bullets.remove(bullet)

    def draw(self, win):
        rotatedImage = self.image.copy()
        if self.angle > 90 or self.angle < -90:
            rotatedImage = pg.transform.flip(rotatedImage, False, True)
        rotatedImage = pg.transform.rotozoom(rotatedImage, self.angle, 1)
        win.blit(rotatedImage, self.rect)
        for bullet in self.bullets:
            pg.draw.rect(win, self.bullColor, bullet[1])

        if self.closest != None:
            pg.draw.rect(win, (255,50,80), self.target.rect, 5)

