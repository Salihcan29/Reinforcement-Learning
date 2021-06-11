# -*- coding: utf-8 -*-

import pygame


class Player(pygame.sprite.Sprite):
    # sprite for the player
    def __init__(self, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.__x = x
        self.__y = y
        
    def update(self, action):
        if action == 0:
            self.__x += 1
        elif action == 1:
            self.__x -= 1
        elif action == 2:
            self.__y += 1
        elif action == 3:
            self.__y -= 1
        elif action == 4:
            self.__x += 1
            self.__y += 1
        elif action == 5:
            self.__x -= 1
            self.__y -= 1
        elif action == 6:
            self.__x -= 1
            self.__y += 1
        elif action == 7:
            self.__x += 1
            self.__y -= 1

        self.rect.x = self.__x * 10
        self.rect.y = self.__y * 10

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y
