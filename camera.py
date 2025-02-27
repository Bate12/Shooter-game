import pygame

#CODE FROM https://stackoverflow.com/questions/21371844/python-pygame-player-is-always-centered

class Camera:
    def __init__(self, width, height, background):
        self.offset = pygame.math.Vector2() 
        self.width = width
        self.height = height
        self.background = background
        self.ground_rect = self.background.get_rect(topleft = (0, 0))

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.width//2
        self.offset.y = target.rect.centery - self.height//2

    def custom_draw(self, sprite_group, player, screen):
        self.center_target_camera(player)

        # Blit the background image
        ground_offset = self.ground_rect.topleft - self.offset
        screen.blit(self.background, ground_offset)

        # Blit the sprites
        for sprite in sprite_group:
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)

if __name__ == "__main__":
    quit()