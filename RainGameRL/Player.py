# -*- coding: utf-8 -*-

import pygame
import random
import Raingame

class Player(pygame.sprite.Sprite):
    # sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,20))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.radius = 10
        self.rect.centerx = Raingame.WIDTH/2
        self.rect.bottom = Raingame.HEIGHT - 1
        self.speedx = 0
        
    def update(self, action):
        self.speedx = 0
        
        if action == 0:
            self.speedx = -4
        elif action == 1:
            self.speedx = 4
        else:
            self.speedx = 0
            
        self.rect.x +=self.speedx
        
        if self.rect.right > Raingame.WIDTH:
            self.rect.right = Raingame.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
    def getCoordinates(self):
        return (self.rect.x, self.rect.y)
    
