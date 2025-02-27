import pygame, math
from random import randint, choice
from player import Player
from object import Object
from enemy import Enemy
from enemy_shooter import EnemyShooter
from text import Text
from levels import Leveles
from settings import *


class Game():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Epická semestrálka")

        iconImage = pygame.image.load('assets/player.png')
        pygame.display.set_icon(iconImage)

        self.bgImage = pygame.image.load("assets/bg_image.png")
        self.bgImage2 = pygame.image.load("assets/bg_image2.png")

        self.tileSize = 200

        self.restartText = Text('"R" to restart', HALFWIDTH, HALFHEIGHT)
        self.restartText.isVisable = False

        self.score = 0
        self.scoreText = Text(f"{self.score}", HALFWIDTH, 20, 40)
        
        self.running = True
        self.win=pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
 
        self.player = Player(self, (HALFWIDTH, HALFHEIGHT), GENERAL_SIZE)
        self.enemies = []

        self.background = Object(self, (50, 50), WIDTH - 100, HEIGHT - 100, color=(BG_COLOR), isCentered=False)
        self.allSprites = pygame.sprite.Group()
        self.playerGroup = pygame.sprite.GroupSingle(self.player)
        #self.allSprites.add(self.background)
        #self.allSprites.add(self.player)

        self.shoot = False

        self.timeTotal = 0
        self.spawnCD = 1.5 # seconds
        self.spawnEstimate = 0
        
        self.levels = Leveles()
        self.lvlText = Text(f"Level {self.levels.lvl}", HALFWIDTH, 60, 40)
        self.lvlUpInterval = 10

        self.spawnVariety = 10
        self.spawnCount = 1
        self.enemySpeed = 2.5
        self.enemyProjectileSpeed = 5

        self.shootEvent = pygame.USEREVENT + 1
        self.shootCD = 800
        pygame.time.set_timer(self.shootEvent, self.shootCD) 

    def drawBackground(self):
        for x in range(0, WIDTH, self.tileSize):
            for y in range (0, HEIGHT, self.tileSize):
                self.win.blit(self.bgImage2, (x, y))

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

        self.levels.lvl = 0
        self.levels.increaseLevel(self)
        self.lvlText.update(f"Level {self.levels.lvl}")

    def levelHandler(self):
        if self.score % self.lvlUpInterval == 0:
            print("LEVEL UP")
            self.levels.increaseLevel(self)
        self.lvlText.update(f"Level {self.levels.lvl}")
          
    def Render(self):
        self.drawBackground()
        self.allSprites.draw(self.win)
    
        for e in self.enemies:
            e.render(self.win)

        self.player.draw(self.win)

        self.restartText.render(self.win)
        self.scoreText.render(self.win)
        self.lvlText.render(self.win)

        pygame.display.flip()

    def Update(self):
        self.allSprites.update()

    def enemySpawner(self):
        if self.timeTotal > self.spawnEstimate:
            self.spawnEstimate += self.spawnCD
            for i in range(self.spawnCount):
                self.spawnEnemy()


    def eventHandler(self):
        self.mPos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            #if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #    self.shoot = True
                    
            if event.type==pygame.QUIT:
                self.running = False

            if event.type == self.shootEvent:
                self.shoot = True


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
        pos = self.getPosOutsideBounds(GENERAL_SIZE)
        # Randomly choose between Enemy and EnemyShooter
        if randint(0, self.spawnVariety) == 0:
            shoot_cd = randint(10, 30) / 10  # Náhodný cooldown mezi 1.0 a 3.0 sekundami
            self.enemies.append(EnemyShooter(pos, GENERAL_SIZE, 1, shoot_cd, self.enemyProjectileSpeed)) # projectile speed nefunguje jak má
        else:
            self.enemies.append(Enemy(pos, GENERAL_SIZE, self.enemySpeed))

    def mainLoop(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 100
            self.timeTotal += self.dt / 10

            self.keys = pygame.key.get_pressed()

            self.eventHandler()

            self.scoreText.update(f"{self.score}")

            if self.player.alive:
                self.playerGroup.update()
                self.player.enemyColCheck(self.enemies, self.player.gun.bullets)
                self.enemySpawner()
                
                # Kontrola kolize hráče s nepřátelskými projektily
                for e in self.enemies:
                    if isinstance(e, EnemyShooter):
                        e.update(self.player, self.timeTotal)
                        for bullet in e.bullets:
                            if not bullet.friendly and self.player.rect.colliderect(bullet.rect):
                                self.player.alive = False  # Hráč umírá
                                pygame.mixer.Sound.play(self.player.hurtSFX).set_volume(VOLUME)
                    else:
                        e.update(self.player)
            else:
                self.restartText.isVisable = True

            if not self.player.alive and self.keys[ord("r")]:
                self.restart()

            self.shoot = False

            self.Update()
            self.Render()

g = Game()
if __name__ == "__main__":
    g.mainLoop()

pygame.quit()