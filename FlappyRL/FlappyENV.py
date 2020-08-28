# -*- coding: utf-8 -*-

import numpy as np
import pygame
import random
import Bird
import Barrier

# hyper parameters
WIDTH = 360
HEIGHT = 640
FPS = 60

class FlappyENV():
    def __init__(self):
        self.episode = 0

        self.ground = pygame.Rect(0, 512, WIDTH, 640)
        
        self.player = Bird.Bird()
        self.players = pygame.sprite.Group()
        self.players.add(self.player)
        self.barriers = pygame.sprite.Group()
        self.time = 0
        pygame.init()
        self.clock = pygame.time.Clock()
        self.reward = 0
        self.done = False
    
    def findDistance(self, a, b):
        d = a-b
        return d
    
    def getState(self):
        if(len(self.barriers) == 0):
            return np.array([0,0,0])
        
        cors = [self.player.vy,self.player.ay]
        
        if(self.findDistance(self.barriers.sprites()[1].rect.right,self.player.rect.left)>0):
            cors.append(self.findDistance(self.player.rect.bottom,self.barriers.sprites()[1].rect.top+5))
        else:
            cors.append(self.findDistance(self.player.rect.bottom,self.barriers.sprites()[3].rect.top+5))
        
        return np.array(cors)
        
    def reset(self):
        self.episode += 1
        self.time = 0
        self.player = Bird.Bird()
        self.players = pygame.sprite.Group()
        self.players.add(self.player)
        self.barriers = pygame.sprite.Group()
        return self.getState()
        
    def close(self): 
        pygame.quit()

    def step(self,action):
        self.reward = 0
        self.barriers.update(self)
            
        self.player.update(action,self)
        
        if self.time == 0:
            height = random.randint(0,360)
            self.barriers.add(Barrier.Barrier(self,512-height-125,True,x = WIDTH))
            self.barriers.add(Barrier.Barrier(self,height,False,x = WIDTH))
            height = random.randint(0,360)
            self.barriers.add(Barrier.Barrier(self,512-height-125,True,x = WIDTH+225))
            self.barriers.add(Barrier.Barrier(self,height,False,x = WIDTH+225))
        
        if len(self.barriers) < 4:
            self.reward += 3000
            height = random.randint(0,360)
            self.barriers.add(Barrier.Barrier(self,512-height-125,True,x = WIDTH+40))
            self.barriers.add(Barrier.Barrier(self,height,False,x = WIDTH+40))
            
            
        hits = pygame.sprite.spritecollide(self.player,self.barriers,False, pygame.sprite.collide_rect)   
        
        done = False
        if hits:
            self.reward -= 0
            done = True

        if self.player.rect.bottom >= 512:
            self.reward -= 0
            
            done = True
            
        self.reward += 0
        
        if self.time == 3600:
            done = True
        
        self.time += 1
        next_state = self.getState()
        return next_state, self.reward, done
        
        
    def initer(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("FlappyRL Game")
        self.render()
        
    def render(self):
        self.clock.tick(60)
        self.screen.fill((52, 152, 219))
        pygame.draw.rect(self.screen,(39, 174, 96),self.ground)
        self.players.draw(self.screen)
        self.barriers.draw(self.screen)
        
        font = pygame.font.Font(None, 32)
        text = font.render("Episode: "+str(self.episode), True, (0,0,0))
        textRect = text.get_rect()
        textRect.left = 30
        textRect.top = 30
        self.screen.blit(text, textRect)
          
        
        pygame.display.flip()