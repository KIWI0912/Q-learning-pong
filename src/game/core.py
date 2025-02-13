class Game:
    def __init__(self):
        self.balls = []
        self.paddle = None
        self.rewards = []
        self.score = 0
        self.time_elapsed = 0
        
    def reset(self):
        self.balls = [Ball()]
        self.paddle = Paddle()
        self.rewards = [Reward() for _ in range(5)]
        self.score = 0
        self.time_elapsed = 0
        
    def update(self, action):
        # Update sphere position
        for ball in self.balls[:]:
            ball.x += ball.vx
            ball.y += ball.vy
            
            # Boundary treatment
            if ball.x <= 0 or ball.x >= SCREEN_WIDTH:
                ball.vx = -ball.vx
            if ball.y <= 0:
                ball.vy = -ball.vy
            if ball.y >= SCREEN_HEIGHT:
                self.balls.remove(ball)
                if not self.balls:
                    self.score -= 10
                    self.balls.append(Ball())
                    
            # Baffle collision
            if check_ball_collision(ball, self.paddle):
                ball.vy = -abs(ball.vy)
                self.score += 5
                
            # Reward collected
            for reward in self.rewards:
                if check_reward_collision(ball, reward):
                    reward.active = False
                    self.apply_reward(reward)
