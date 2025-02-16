import numpy as np
import random

class QAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.actions = actions
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.Q = {}  # Q-table

    def get_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)  # Explore
        else:
            return self.get_best_action(state)  # Exploit

    def get_best_action(self, state):
        if state not in self.Q:
            self.Q[state] = np.zeros(len(self.actions))
        return np.argmax(self.Q[state])

    def update(self, state, action, reward, next_state):
        if state not in self.Q:
            self.Q[state] = np.zeros(len(self.actions))
        if next_state not in self.Q:
            self.Q[next_state] = np.zeros(len(self.actions))

        # Q-learning update rule
        best_next_action = np.argmax(self.Q[next_state])
        self.Q[state][action] += self.alpha * (reward + self.gamma * self.Q[next_state][best_next_action] - self.Q[state][action])
