import pygame, math
from random import randint
from settings import *

from enemy import Enemy
from projectile import Projectile

class EnemyShooter(Enemy):
    def __init__(self, game, pos, size, speed, shoot_cd=1.5, shootSpeed=5):
        super().__init__(game, pos, size, speed, color=(20, 0, 250))
        self.shoot_cd = shoot_cd  # Cooldown mezi střelami (v sekundách)
        self.shootSpeed = shootSpeed
        self.last_shot_time = randint(0, int(shoot_cd * 1000)) / 1000  # Náhodný časovač
        self.bullets = []
    
    def shoot(self, player, current_time, shootSpeed):
        if current_time - self.last_shot_time >= self.shoot_cd:
            direction = player.pos - self.pos
            new_bullet = Projectile(self.rect.center, direction, shootSpeed, 10, friendly=False)  # Nepřátelský projektil
            self.bullets.append(new_bullet)
            self.last_shot_time = current_time  # Reset časovače
    
    def update(self):
        super().update()
        self.shoot(self.game.player, self.game.timeTotal, self.shootSpeed)
        
        # Aktualizace projektilů
        for bullet in self.bullets:
            bullet.update()
    
    def render(self, win):
        win.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.render(win)