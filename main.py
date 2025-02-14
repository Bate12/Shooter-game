import pygame, math
from random import randint, choice
from player import Player
from enemy import Enemy
from text import Text
from settings import *


class Game():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Epická semestrálka")

        self.restartText = Text('"R" to restart', HALFWIDTH, HALFHEIGHT)
        self.restartText.isVisable = False

        self.score = 0
        self.scoreText = Text(f"{self.score}", HALFWIDTH, 20, 40)
        
        self.running = True
        self.win=pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.generalSize = 20
 
        self.player = Player((HALFWIDTH, HALFHEIGHT), self.generalSize)
        self.enemies = []

        self.shoot = False

        self.timeTotal = 0
        self.spawnCD = 1.5 # seconds
        self.spawnEstimate = 0


    def restart(self):
        self.restartText.isVisable = False

        self.player.alive = True
        self.player.pos.x = HALFWIDTH
        self.player.pos.y = HALFHEIGHT
        self.player.vel = pygame.Vector2()

        self.enemies = []
        self.player.gun.bullets = []

        self.spawnEstimate = self.timeTotal
        self.score = 0
        
        
    def Render(self):
        self.win.fill((255,255,255))
        self.player.render(self.win)

        for e in self.enemies:
            e.render(self.win)

        self.restartText.render(self.win)
        self.scoreText.render(self.win)

        pygame.display.flip()

    def enemySpawner(self):
        if self.timeTotal > self.spawnEstimate:
            self.spawnEstimate += self.spawnCD
            self.spawnEnemy()
            self.spawnEnemy()

    def eventHandler(self):
        global mPos
        for event in pygame.event.get():
            mPos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.shoot = True
                
            if event.type==pygame.QUIT:
                self.running=False

    def getPosOutsideBounds(self, padding):
        side = choice(["left", "right", "top", "bottom"])

        if side == "left":
            x = -padding
            y = randint(0, HEIGHT)
        elif side == "right":
            x = WIDTH + padding
            y = randint(0, HEIGHT)
        elif side == "top":
            x = randint(0, WIDTH)
            y = -padding
        elif side == "bottom":
            x = randint(0, WIDTH)
            y = HEIGHT + padding

        return x, y

    def spawnEnemy(self):
        pos = self.getPosOutsideBounds(self.generalSize)
        self.enemies.append(Enemy(pos, self.generalSize, 2.5))

    def mainLoop(self):
        while self.running:
            dt = self.clock.tick(FPS) / 100
            self.timeTotal += dt / 10

            keys = pygame.key.get_pressed()

            self.eventHandler()

            self.scoreText.update(f"{self.score}")

            if self.player.alive:
                self.player.update(keys, dt, mPos, self.shoot)
                self.player.enemyColCheck(self.enemies, self.player.gun.bullets, self)
                self.enemySpawner()
                
                for e in self.enemies:
                    e.update(self.player)
            else:
                self.restartText.isVisable = True

            if not self.player.alive and keys[ord("r")]:
                self.restart()

            self.shoot = False

            self.Render()

g = Game()
if __name__ == "__main__":
    g.mainLoop()



pygame.quit()
