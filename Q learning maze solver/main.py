# -*- coding: utf-8 -*-

import yazlabgame
import numpy as np
import matplotlib.pyplot as plt
import time

env = yazlabgame.Environment(100, 70)
env.initer()

# Q table
q_table = np.zeros((env.observation_space_n, env.action_space_n))

# hyper parameters
gamma = 0.9

# plotting Matrix
reward_list = []
success_list = []

episode_number = 117431

before_repetition = 0
repetition_c = 0

for episode in range(1, episode_number):

    # initialize environment
    state = env.reset()

    total_reward = 0

    while True:

        action = np.argmax(q_table[state])
        # action process and take reward / observation
        next_state, reward, done = env.step(action)

        # Q learning function
        old_value = q_table[state, action]  # old value
        next_max = np.max(q_table[next_state])  # next_max
        new_value = reward + gamma * next_max

        # Q table update
        q_table[state, action] = new_value

        # update state
        state = next_state

        total_reward += reward

        if episode % 2167 < 2:
            env.render(episode)

        if done:
            if reward == 5:
                success_list.append(1)
            else:
                success_list.append(0)

            if episode % 14 == 0:
                env.render(episode)
            reward_list.append(total_reward)
            print("Episode: {}, reward: {}, success: {}".format(episode, total_reward, reward == 5))
            break

    if total_reward == before_repetition:
        repetition_c += 1
    else:
        before_repetition = total_reward
        repetition_c = 1

    if repetition_c == 100:
        break

# %% visualize render

state = env.reset()
while True:
    action = np.argmax(q_table[state])
    state, reward, done = env.step(action)
    env.render('Best params!')
    time.sleep(0.04)
    if done:
        break

time.sleep(3)
# %% visualize
fig, axs = plt.subplots(1, 2)

axs[0].scatter(range(len(reward_list)), reward_list)
axs[0].set_xlabel("episode")
axs[0].set_ylabel("reward")

axs[1].scatter(range(len(success_list)), success_list)
axs[1].set_xlabel("episode")
axs[1].set_ylabel("success")

axs[0].grid(True)
axs[1].grid(True)

plt.tight_layout()
plt.show()
