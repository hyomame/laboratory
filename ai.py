# -*- coding: utf-8 -*-

import numpy as np
import random
import copy
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam, RMSprop
from collections import deque
from keras import backend as K


class DQN_Solver:
    """
    Multi Layer Perceptron with Experience Replay
    """

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=100000)
        self.gamma = 0.9
        self.epsilon = 1.0
        self.e_decay = 0.9999
        self.e_min = 0.01
        self.learning_rate = 0.0001
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(128, input_shape=(2,2), activation='tanh'))
        model.add(Flatten())
        model.add(Dense(128, activation='tanh'))
        model.add(Dense(128, activation='tanh'))
        model.add(Dense(1, activation='linear'))
        model.compile(loss="mse", optimizer=RMSprop(lr=self.learning_rate))
        return model

    def remember_memory(self, state, action, reward):
        self.memory.append((state, action, reward))

    def choose_action(self, state, movables):
        if self.epsilon >= random.random():
            return random.choice(movables)
        else:
            return self.choose_best_action(state, movables)
        
    def choose_best_action(self, state, movables):
        best_actions = []
        max_act_value = -100
        for a in movables:
            np_action = np.array([[state, a]])
            act_value = self.model.predict(np_action)
            if act_value > max_act_value:
                best_actions = [a,]
                max_act_value = act_value
            elif act_value == max_act_value:
                best_actions.append(a)
        return random.choice(best_actions)

    def replay_experience(self, batch_size):
        batch_size = min(batch_size, len(self.memory))
        minibatch = random.sample(self.memory, batch_size)
        X = []
        Y = []
        for i in range(batch_size):
            state, action, reward, next_state, next_movables, done = minibatch[i]
            input_action = [state, action]
            if done:
                target_f = reward
            else:
                next_rewards = []
                for i in next_movables:
                    np_next_s_a = np.array([[next_state, i]])
                    next_rewards.append(self.model.predict(np_next_s_a))
                np_n_r_max = np.amax(np.array(next_rewards))
                target_f = reward + self.gamma * np_n_r_max
            X.append(input_action)
            Y.append(target_f)
        np_X = np.array(X)
        np_Y = np.array([Y]).T
        self.model.fit(np_X, np_Y, epochs=1, verbose=0)
        if self.epsilon > self.e_min:
            self.epsilon *= self.e_decay