class QLearning:
    def __init__(self):
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1
        self.Q = {}
        
    def get_state(self, balls, paddle):
        if not balls:
            return None
            
        closest_ball = min(balls, key=lambda b: (SCREEN_HEIGHT - b.y) / abs(b.vy) 
                          if b.vy != 0 else float('inf'))
        
        return (
            int(closest_ball.x // 50),
            int(closest_ball.y // 50),
            int(paddle.x // 50),
            1 if closest_ball.vx > 0 else -1,
            1 if closest_ball.vy > 0 else -1
        )
        
    def choose_action(self, state):
        if state not in self.Q:
            self.Q[state] = {a: 0 for a in [-1, 0, 1]}
            
        if random.uniform(0, 1) < self.epsilon:
            return random.choice([-1, 0, 1])
        else:
            return max(self.Q[state], key=self.Q[state].get)
            
    def update(self, state, action, reward, next_state):
        if state not in self.Q:
            self.Q[state] = {a: 0 for a in [-1, 0, 1]}
        if next_state not in self.Q:
            self.Q[next_state] = {a: 0 for a in [-1, 0, 1]}
            
        current_q = self.Q[state][action]
        max_next_q = max(self.Q[next_state].values())
        self.Q[state][action] = current_q + self.alpha * (
            reward + self.gamma * max_next_q - current_q)
