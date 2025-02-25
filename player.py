import pygame as pg
from settings import *
from gun import Gun
from object import Object

class Player(Object):
    def __init__(self, game, pos, size):
        # Call the parent class constructor properly
        super().__init__(game, pos, size, isCentered=True)
        
        # Player-specific attributes
        self.vel = pg.Vector2()
        self.acc = pg.Vector2()
        self.size = size
        self.halfSize = self.size // 2
        self.alive = True

        self.friction = -0.6
        self.accspeed = 40
        self.maxspeed = 50
        
        self.color = (255, 0, 255)
        
        self.hurtSFX = pg.mixer.Sound("assets/hitHurt.wav")
        self.hitSFX = pg.mixer.Sound("assets/explosion.wav")

        self.image = pg.image.load("assets/player.png")
        self.image = pg.transform.scale(self.image, (self.size, self.size))

        self.game = game

        self.gun = Gun(self.game, self)
        self.gunDistance = 30

        self.updateRect()

    def updateRect(self):
        # Centered position adjustment
        if self.isCentered:
            self.rect.center = self.pos
        else:
            self.rect.topleft = self.pos

    def gunHandler(self):
        # Get mouse position and shoot state from the Game object
        mpos = self.game.mPos
        shoot = self.game.shoot

        dist = pg.Vector2(mpos[0] - (self.pos.x + self.halfSize), mpos[1] - (self.pos.y + self.halfSize))
        dist.normalize_ip()

        if shoot:
            self.gun.shoot(dist)
            dist.scale_to_length(0.5)
        
        dist *= self.gunDistance
        
        self.gun.pos = self.rect.center + dist - (self.gun.halfSize, self.gun.halfSize)
        self.gun.rotateTo(dist)
        self.gun.updateRect()

        for b in self.gun.bullets:
            b[0] += b[2] * self.gun.shootVel
            b[1].topleft = b[0] 

        self.gun.bullets = [b for b in self.gun.bullets if 0 < b[0].x < WIDTH and 0 < b[0].y < HEIGHT]

    def update(self):
        self.acc = pg.Vector2()
        
        # Movement handling
        if self.game.keys[ord("w")]:
            self.acc.y -= self.accspeed
            
        if self.game.keys[ord("s")]:
            self.acc.y += self.accspeed
            
        if self.game.keys[ord("d")]:
            self.acc.x += self.accspeed
            
        if self.game.keys[ord("a")]:
            self.acc.x -= self.accspeed

        # Physics calculations
        self.acc += self.vel * self.friction
        self.vel += self.acc * self.game.dt
        self.limit_vel(self.maxspeed)

        self.pos += self.vel * self.game.dt + (self.acc * 0.5) * (self.game.dt * self.game.dt)

        self.inScreenCheck()
        self.updateRect()

        self.gun.update()
        self.gunHandler()

    def limit_vel(self, max_vel):
        try:
            self.vel = self.vel.clamp_magnitude(self.maxspeed)
        except ValueError:
            self.vel = pg.Vector2(0, 0)

    def inScreenCheck(self):
        # Screen boundary checks
        if self.pos.x < 0:
            self.vel.x = 0
            self.pos.x = 0

        if self.pos.y < 0:
            self.vel.y = 0
            self.pos.y = 0

        if self.pos.x > WIDTH - self.size:
            self.vel.x = 0
            self.pos.x = WIDTH - self.size

        if self.pos.y > HEIGHT - self.size:
            self.vel.y = 0
            self.pos.y = HEIGHT - self.size

    def enemyColCheck(self, enemies, bullets):
        # Collision with enemies
        for e in enemies[:]:
            if self.rect.colliderect(e.rect):
                self.alive = False
                pg.mixer.Sound.play(self.hurtSFX).set_volume(VOLUME)
                return 
        
        # Bullet and enemy collision
        for e in enemies[:]:
            for b in bullets[:]:
                if b[1].colliderect(e.rect):
                    pg.mixer.Sound.play(self.hitSFX).set_volume(VOLUME)
                    enemies.remove(e)
                    bullets.remove(b)
                    self.game.score += 1
                    self.game.levelHandler()
                    break

    def draw(self, win):
        win.blit(self.image, self.rect)
        self.gun.draw(win)


if __name__ == "__main__":
    quit()
