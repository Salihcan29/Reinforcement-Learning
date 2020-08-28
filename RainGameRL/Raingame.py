# -*- coding: utf-8 -*-

import numpy as np
import pygame
import random
import Player
import Enemy

# hyper parameters
WIDTH = 360
HEIGHT = 360
FPS = 60
class Raingame():
    def __init__(self):
        self.player = Player.Player()
        self.players = pygame.sprite.Group()
        self.players.add(self.player)
        self.enemies = pygame.sprite.Group()
        self.time = 0
        pygame.init()
        self.clock = pygame.time.Clock()
        self.reward = 0
        self.done = False
    
    def findDistance(self, a, b):
        d = a-b
        return d
    
    def getState(self):
        player = self.player.getCoordinates()
        cors = []
        
        for index,e in enumerate(self.enemies):
            if index > 2:
                break
            cors.append(self.findDistance(player[0],e.getCoordinates()[0]))
            cors.append(self.findDistance(player[1],e.getCoordinates()[1]))
        
        for i in range(6-len(cors)):
            cors.append(999)
        return np.array(cors)
        
    def reset(self):
        self.time = 0
        self.player = Player.Player()
        self.players = pygame.sprite.Group()
        self.players.add(self.player)
        self.enemies = pygame.sprite.Group()
        return self.getState()
        
    def close(self): 
        pygame.quit()

    def step(self,action):
        self.enemies.update(self)
        self.player.update(action)
        self.time += 1
        
        if len(self.enemies) == 0:
            self.enemies.add(Enemy.Enemy(self))
            self.enemies.add(Enemy.Enemy(self))
            self.enemies.add(Enemy.Enemy(self))
            self.enemies.add(Enemy.Enemy(self))
            
        hits = pygame.sprite.spritecollide(self.player,self.enemies,False, pygame.sprite.collide_circle)   
        
        reward = 0
        done = False
        if hits:
            reward = -10
            done = True
            
        if self.time % 360 == 0:
            reward += 1
        if self.time == 3600:
            done = True
            
        next_state = self.getState()
        return next_state, reward, done
        
        
    def initer(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("RL Game")
        self.render()
        
    def render(self):
        self.clock.tick(60)
        self.screen.fill((0,200,0))
        self.players.draw(self.screen)
        self.enemies.draw(self.screen)
        pygame.display.flip()