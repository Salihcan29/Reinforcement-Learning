# -*- coding: utf-8 -*-

import pygame
import random
import Raingame

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self,env):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.radius = 5
        pygame.draw.circle(self.image, (255,255,255), self.rect.center,self.radius)
        self.rect.x = random.randrange(0, Raingame.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-Raingame.HEIGHT, -self.rect.height)
        
        self.speedy = 3
    
    def update(self,env):

        self.rect.y += self.speedy
        
        if self.rect.top > Raingame.HEIGHT + 10:
            self.rect.x = random.randrange(0, Raingame.WIDTH - self.rect.width)
            self.rect.y = 0
        
            
    def getCoordinates(self):
        return (self.rect.x, self.rect.y)  
    
        
