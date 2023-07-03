import gym
import random
import numpy as np
import time
from collections import deque
import pickle

from collections import defaultdict

EPISODES = 20000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999


def default_Q_value():
    return 0


if __name__ == "__main__":

    random.seed(1)
    np.random.seed(1)
    env = gym.envs.make("FrozenLake-v1")
    env.seed(1)
    env.action_space.np_random.seed(1)

    # You will need to update the Q_table in your iteration
    Q_table = defaultdict(default_Q_value)  # starts with a pessimistic estimate of zero reward for each state.
    episode_reward_record = deque(maxlen=100)

    for i in range(EPISODES):
        episode_reward = 0
        done = False
        obs = env.reset()

        while (not done):
            # Choose the action that maximizes the expected future reward
            if np.random.uniform(0, 1) < EPSILON:
                action = env.action_space.sample()  # Explore
            else:
                q_values = [Q_table[(obs, a)] for a in range(env.action_space.n)]
                action = np.argmax(q_values)  # Exploit

            # Take the action and observe the new state, reward, and done flag
            new_obs, reward, done, info = env.step(action)
            episode_reward += reward  # update episode reward

            # Update the Q_table using Q-Learning
            if done:
                target = reward
            else:
                target = reward + DISCOUNT_FACTOR * max([Q_table[(new_obs, a)] for a in range(env.action_space.n)])
            Q_table[(obs, action)] = (1 - LEARNING_RATE) * Q_table[(obs, action)] + LEARNING_RATE * target

            # Update the current state to the new state
            obs = new_obs

        # Decay the exploration rate
        EPSILON *= EPSILON_DECAY

        # record the reward for this episode
        episode_reward_record.append(episode_reward)

        if i % 100 == 0 and i > 0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record)) / 100))
            print("EPSILON: " + str(EPSILON))

    #### DO NOT MODIFY ######
    model_file = open('Q_TABLE.pkl', 'wb')
    pickle.dump([Q_table, EPSILON], model_file)
    model_file.close()
    #########################
