import pygame
from settings import *
from spritesheets import *
import random

class Enemies(pygame.sprite.Sprite):
    def __init__(self,game):
        self.groups=game.enemies
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game=game
        self.spritesheetsobj = SpriteSheet()
        self.image_up = pygame.image.load('doodler-pirate/data/parrot1.png').convert_alpha()
        self.image_up.set_colorkey(black)

        self.image=self.image_up
        self.rect=self.image.get_rect()
        self.rect.centerx=random.choice([-100,display_width+100])
        self.vx=random.randrange(1,4)
        if self.rect.centerx>display_width:
            self.vx=-self.vx
        self.rect.y=random.randrange(0,display_height/2)
        self.vy=0
        self.dy=0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy = -self.dy
        
        center = self.rect.center
        
        if self.vx > 0:  # If moving right
            self.image = pygame.transform.flip(self.image_up, True, False)
        else:
            self.image = self.image_up  # Reset image to default
        
        if self.dy < 0:
            self.image = pygame.transform.flip(self.image, False, True)  # Flip vertically when moving up
        else:
            self.image = pygame.transform.flip(self.image, False, False)  # Reset flip
        
        self.rect = self.image.get_rect()
        self.mask_image = pygame.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy
        
        if self.rect.left > display_width + 100 or self.rect.right < -100:
            self.kill()