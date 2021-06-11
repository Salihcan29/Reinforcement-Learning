# -*- coding: utf-8 -*-

import numpy as np
import pygame
import random
import Player


class Environment:
    def __init__(self, m, n):
        self.observation_space_n = m*n
        self.action_space_n = 4  # 8 for 8 sides

        self.n = n
        self.m = m
        self.width = m*10
        self.height = n*10

        self.startY = int(input("Enter start position Y: "))
        self.targetY = int(input("Enter target position Y: "))

        self.player = Player.Player(0, self.startY)

        self.map = np.zeros((n, m))
        self.rewards = np.zeros((n, m))
        self.drawWall(self.map, self.rewards)

        self.cordmemory = {}
        self.players = pygame.sprite.Group()
        self.players.add(self.player)
        self.time = 0
        pygame.init()

        pygame.font.init()
        self.myfont = pygame.font.SysFont('Helvetica', 30)

    def getState(self):
        return self.player.getX()*self.n+self.player.getY()

    def reset(self):
        self.time = 0
        self.player = Player.Player(20, self.startY)
        self.players = pygame.sprite.Group()
        self.players.add(self.player)
        self.cordmemory = {}
        return self.getState()

    def step(self, action):
        self.cordmemory[(self.player.getX(), self.player.getY())] = 1

        self.player.update(action)
        self.time += 1

        done = False
        try:
            reward = self.rewards[self.player.getY()][self.player.getX()]
        except IndexError:
            pass

        if self.player.getX() > self.m-1 or self.player.getX() < 0 or \
                self.player.getY() < 0 or self.player.getY() > self.n-1 or \
                self.map[self.player.getY()][self.player.getX()] == 1:
            if action == 0 or action == 1:
                self.player.update(-action+1)
            elif action == 2 or action == 3:
                self.player.update(-action+5)
            elif action == 4 or action == 5:
                self.player.update(-action+9)
            elif action == 6 or action == 7:
                self.player.update(-action+13)
            reward = -5
            done = True

        if (self.player.getX() == self.m-1 and self.player.getY() == self.targetY) or self.time == 3600:
            done = True

        next_state = self.getState()
        return next_state, reward, done

    def drawWall(self, map, rewards):
        cords = [(i, j) for j in range(self.m) for i in range(self.n)]
        random.shuffle(cords)

        for i in range(int(self.m*self.n*0.3)):
            coordinate = cords.pop()
            map[coordinate[0]][coordinate[1]] = 1

        for i in range(self.n):
            for j in range(self.m):
                rewards[i][j] = -1 if map[i][j] == 0 else -5

        map[self.startY][20] = 0
        map[self.targetY][self.m-1] = 0
        rewards[self.startY][20] = -1
        rewards[self.targetY][self.m-1] = 5

        file = open('engel.txt', 'w')

        for i in range(self.n):
            for j in range(self.m):

                if self.player.getY() == i and self.player.getX() == j:
                    file.write('  O')
                elif self.targetY == i and j == self.m:
                    file.write('  H')
                elif map[i][j] == 0:
                    file.write('  D')
                elif map[i][j] == 1:
                    file.write('  Y')

            file.write('\n')

    def initer(self):
        pygame.display.set_caption("Q Learning")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.render(1)

    def render(self, episode):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (0,0, self.width, self.height))

        for i in range(self.m):
            for j in range(self.n):
                if self.map[j][i] == 0:
                    pygame.draw.rect(self.screen,(127,140,141),(i*10+1,j*10+1,9,9))
                elif self.map[j][i] == 1:
                    pygame.draw.rect(self.screen, (44, 62, 80), (i * 10 + 1, j * 10 + 1, 9, 9))

        for cord in self.cordmemory:
            pygame.draw.rect(self.screen, (0, 0, 128), (cord[0] * 10 + 1, cord[1] * 10 + 1, 9, 9))

        self.players.draw(self.screen)
        pygame.draw.rect(self.screen, (255, 0, 0), (20 * 10 + 1, self.startY * 10 + 1, 9, 9))
        pygame.draw.rect(self.screen, (255,0,0), ((self.m-1)*10+1,self.targetY*10+1,9,9))
        self.screen.blit(self.myfont.render('Episode: '+str(episode), True, (255, 255, 255)),(20,20))
        pygame.display.flip()
