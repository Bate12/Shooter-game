import pygame, math
from settings import *
from gun import Gun

class Player():
    def __init__(self, pos, size):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2()
        self.size = size
        self.halfSize = self.size//2
        self.alive = True

        self.friction = -0.5
        self.accspeed = 30
        self.maxspeed = 50
        
        self.color = (255,0,255)

        self.hurtSFX = pygame.mixer.Sound("assets/hitHurt.wav")
        self.hitSFX = pygame.mixer.Sound("assets/explosion.wav")

        self.image = pygame.image.load("assets/player.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        self.gun = Gun()

    def updateRect(self):
        self.rect = pygame.Rect(self.pos.x ,self.pos.y, self.size, self.size)

    def gunHandler(self, mpos, shoot):
        dist = pygame.Vector2(mpos[0] - (self.pos.x + self.halfSize), mpos[1] - (self.pos.y + self.halfSize))
        dist.normalize_ip()
        #dist = dist.rotate(90)
        
        dist*= 25
        
        self.gun.pos = self.rect.center + dist - (self.gun.halfSize, self.gun.halfSize)
        self.gun.rotateTo(dist)
        self.gun.updateRect()

        if shoot:
            self.gun.shoot(dist)

        for b in self.gun.bullets:
            b[0] += b[2] * self.gun.shootVel
            b[1].topleft = b[0] 

        self.gun.bullets = [b for b in self.gun.bullets if 0 < b[0].x < WIDTH and 0 < b[0].y < HEIGHT]

    def update(self, keys , dt, mpos, shoot):
        self.acc = pygame.Vector2()
        
        if keys[ord("w")]:
            self.acc.y -= self.accspeed
            
        if  keys[ord("s")]:
            self.acc.y += self.accspeed
            
        if keys[ord("d")]:
            self.acc.x += self.accspeed
            
        if keys[ord("a")]:
            self.acc.x -= self.accspeed

        self.acc += self.vel * self.friction
        self.vel += self.acc * dt
        self.limit_vel(self.maxspeed)

        self.pos += self.vel * dt + (self.acc * 0.5) * (dt * dt)

        self.inScreenCheck()
        self.updateRect()
        self.gunHandler(mpos, shoot)

    def limit_vel(self, max_vel):
        try:
            self.vel = self.vel.clamp_magnitude(self.maxspeed)
        except:
            pass

    def inScreenCheck(self):
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


    def enemyColCheck(self, enemies, bullets, game):
        for e in enemies[:]:
            if self.rect.colliderect(e.rect):
                self.alive = False
                pygame.mixer.Sound.play(self.hurtSFX).set_volume(VOLUME)
                return 
        
        for e in enemies[:]:
            for b in bullets[:]:
                if b[1].colliderect(e.rect):
                    pygame.mixer.Sound.play(self.hitSFX).set_volume(VOLUME)
                    enemies.remove(e)
                    bullets.remove(b)
                    game.score += 1
                    game.levelHandler()
                    break

        
            
    def render(self, win):
        win.blit(self.image, self.rect)
        #pygame.draw.rect(win, self.color, self.rect)
        #pygame.draw.rect(win, self.gun.color, self.gun.rect)
        self.gun.render(win)
        for b in self.gun.bullets:
            pygame.draw.rect(win, self.gun.bullColor, b[1])

if __name__ == "__main__":
    quit()
