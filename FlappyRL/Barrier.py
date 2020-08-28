# -*- coding: utf-8 -*-

import pygame
import random
import FlappyENV

class Barrier(pygame.sprite.Sprite):
    
    def __init__(self,env,height,up,x = 410):
        pygame.sprite.Sprite.__init__(self)
        self.height = height
        self.image = pygame.Surface((50,self.height))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        if up:
            self.rect.top = 0
        else:
            self.rect.bottom = 512
        
        self.vx = -3
    
    def update(self,env):
        self.rect.x += self.vx
        if self.rect.right < 0:
            self.rect.x = FlappyENV.WIDTH+40
            env.barriers.remove(self)
            
        
            
    def getCoordinates(self):
        return (self.rect.x, self.rect.y)  
    
        
