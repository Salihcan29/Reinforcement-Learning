# -*- coding: utf-8 -*-
"""
Created on Mon May  4 18:20:26 2020

@author: Salihcan
"""
import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from collections import deque

import Raingame
import pygame
import random

class DQLAgent:
    def __init__(self,env):
        # parameter / hyperparameter
        self.state_size = 6
        self.action_size = 2
        
        self.gamma = 0.95
        self.learning_rate = 0.001
        
        self.epsilon = 1
        self.epsilon_decay = 0.998
        self.epsilon_min = 0.01
        
        self.memory = deque(maxlen = 1000)
        
        self.model = self.build_model()
        self.target_model = self.build_model()
    
    def build_model(self):
        # neural network for deep q learning
        model = Sequential()
        model.add(Dense(64,input_dim = self.state_size,activation = "tanh"))
        model.add(Dense(64,activation = "relu"))
        model.add(Dense(64,activation = "relu"))
        model.add(Dense(self.action_size,activation = "linear"))
        model.compile(loss = "mse",optimizer = Adam(learning_rate=self.learning_rate))
        return model
    
    def remember(self, state, action, reward, next_state, done):
        # storage
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        # acting explore or exploit
        if random.uniform(0,1) < self.epsilon:
            return random.randint(0,1)
        else:
            act_values = self.model.predict(state)
            return np.argmax(act_values[0])
            
    
    def replay(self,batch_size):
        "vectorized replay method"
        if len(agent.memory) < batch_size:
            return
        # Vectorized method for experience replay
        minibatch = random.sample(self.memory, batch_size)
        minibatch = np.array(minibatch)
        not_done_indices = np.where(minibatch[:, 4] == False)
        y = np.copy(minibatch[:, 2])

        # If minibatch contains any non-terminal states, use separate update rule for those states
        if len(not_done_indices[0]) > 0:
            predict_sprime = self.model.predict(np.vstack(minibatch[:, 3]))
            predict_sprime_target = self.target_model.predict(np.vstack(minibatch[:, 3]))
            
            # Non-terminal update rule
            y[not_done_indices] += np.multiply(self.gamma, predict_sprime_target[not_done_indices, np.argmax(predict_sprime[not_done_indices, :][0], axis=1)][0])

        actions = np.array(minibatch[:, 1], dtype=int)
        y_target = self.model.predict(np.vstack(minibatch[:, 0]))
        y_target[range(batch_size), actions] = y
        self.model.fit(np.vstack(minibatch[:, 0]), y_target, epochs=1, verbose=0)
            
    
    def adaptiveEGreedy(self):
        # adaptive epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        else:
            self.epsilon = self.epsilon_min


if __name__ == "__main__":
    
    #initialize environment and agent
    env = Raingame.Raingame()
    env.initer()
    agent = DQLAgent(env)

    batch_size = 16
    episode = 3000
    times = []
    for e in range(1,episode):
        # initialize environment
        state = env.reset()
        state = np.reshape(state,[1,state.shape[0]])
        rewards = 0
        time = 0
        while True:
            # act
            action = agent.act(state) # select an action
            
            # step
            next_state, reward, done = env.step(action)
            
            if e % 1 == 0:
                pygame.event.get()
                env.render()
                
            next_state = np.reshape(next_state,[1,next_state.shape[0]])
            
            # remember / storage
            agent.remember(state, action, reward, next_state, done)
            
            # update state
            state = next_state
            
            # replay
            agent.replay(batch_size)
            
            # adjust epsilon
            agent.adaptiveEGreedy()
            rewards += reward
            time += 1
            if done:
                times.append(time)
                print("Episode: {}, Reward: {}, Time: {}".format(e,rewards,time))
                break

#%% matplotlib stats

import matplotlib.pyplot as plt

plt.plot(times)
plt.xlabel('episode')
plt.ylabel('survived time')
plt.show()

#%% test section

import time
trained_model = agent.model
env = Raingame.Raingame()
env.initer()
test_times = []
for e in range(100):
    state = env.reset()
    test_time = 0
    rewards = 0
    while True:
        pygame.event.get()
        state = np.reshape(state,[1,state.shape[0]])
        next_state, reward, done = env.step(np.argmax(trained_model.predict(state)))
        env.render()
        state = next_state
        rewards += reward
        test_time += 1
        if done:
            print("Episode: {}, Reward: {}, Time: {}".format(e,rewards,test_time))
            times.append(test_time)
            break
env.close()