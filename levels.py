class Leveles():
    def __init__(self):
        self.lvl = 1

    def increaseLevel(self, game):
        self.lvl += 1

        if self.lvl == 1:
            game.spawnVariety = 10
            game.spawnCount = 1
            game.enemySpeed = 2.5
            game.enemyProjectileSpeed = 5
        elif self.lvl == 2:
            game.spawnVariety = 7
            game.enemySpeed = 3
            game.enemyProjectileSpeed = 7
        elif self.lvl == 3:
            game.spawnCount = 2
        elif self.lvl == 4:
            game.spawnVariety = 5
            game.enemyProjectileSpeed = 10
        elif self.lvl == 5:
            game.spawnCount = 3
            game.enemySpeed = 4
        elif self.lvl == 6:
            game.spawnVariety = 2
        else:
            game.enemySpeed += 0.5
