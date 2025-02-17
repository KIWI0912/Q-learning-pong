import numpy as np
from ..game.environment import PongEnvironment

class QLearningAgent:
    def __init__(self):
        self.env = PongEnvironment(mode="auto")
        self.q_table = {}  # 状态动作价值表
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 0.1
    
    def get_state(self, ball_pos, paddle_pos):
        # 简化状态空间
        ball_x = int(ball_pos[0] / 100)
        ball_y = int(ball_pos[1] / 100)
        paddle_y = int(paddle_pos[1] / 100)
        return (ball_x, ball_y, paddle_y)
    
    def get_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.choice([-1, 0, 1])  # 随机探索
        
        if state not in self.q_table:
            self.q_table[state] = {-1: 0, 0: 0, 1: 0}
        
        return max(self.q_table[state].items(), key=lambda x: x[1])[0]
    
    def train(self, episodes=1000):
        for episode in range(episodes):
            state = self.get_state(self.env.ball_pos, self.env.paddle_pos)
            total_reward = 0
            
            while True:
                action = self.get_action(state)
                
                # 执行动作
                reward = self.env.step(action)
                next_state = self.get_state(self.env.ball_pos, self.env.paddle_pos)
                
                # Q-learning更新
                if state not in self.q_table:
                    self.q_table[state] = {-1: 0, 0: 0, 1: 0}
                if next_state not in self.q_table:
                    self.q_table[next_state] = {-1: 0, 0: 0, 1: 0}
                
                old_value = self.q_table[state][action]
                next_max = max(self.q_table[next_state].values())
                
                new_value = (1 - self.learning_rate) * old_value + \
                           self.learning_rate * (reward + self.discount_factor * next_max)
                
                self.q_table[state][action] = new_value
                
                total_reward += reward
                state = next_state
                
                if self.env.done:
                    break
            
            if episode % 100 == 0:
                print(f"Episode {episode}, Total Reward: {total_reward}")

def main():
    agent = QLearningAgent()
    print("Starting Q-learning training...")
    agent.train()

if __name__ == "__main__":
    main()
