import pygame
from settings import *

class PowerUps(pygame.sprite.Sprite):
    def __init__(self, platform, game):
        self.groups = game.powerups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = platform
        self.image_normal = pygame.image.load('doodler-pirate/data/spring.png').convert_alpha()
        self.image_comp = pygame.image.load('doodler-pirate/data/spring_comp.png').convert_alpha()
        self.image = self.image_normal
        self.image = pygame.transform.scale(self.image, (133//6, 160//6))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
        self.collided = False

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()
        if pygame.sprite.collide_rect(self, self.game.img_pikachu):
            self.collided = True
            self.image = self.image_comp
        else:
            self.collided = False
            self.image = self.image_normal

        self.image = pygame.transform.scale(self.image, (133//6, 160//6))
