# -*- coding: utf-8 -*-

import pygame
import random
import FlappyENV

class Bird(pygame.sprite.Sprite):
    # sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.radius = 15
        self.rect.centerx = FlappyENV.WIDTH/2
        self.rect.bottom = FlappyENV.HEIGHT/2
        self.rect.x = 40
        self.ay = 0.5
        self.vy = -5
        
    def update(self, action, env):
        self.vy += self.ay
        self.rect.y += self.vy
        
        if self.rect.top > 0 and action == 0:
            env.reward -= 0
            self.vy = -5

        
        if self.rect.bottom > FlappyENV.HEIGHT-128:
            self.rect.bottom = FlappyENV.HEIGHT-128
            self.vy = 0
            
            
    def getCoordinates(self):
        return (self.rect.x, self.rect.y)
    
