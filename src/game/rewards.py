class RewardSystem:
    def __init__(self):
        self.rewards = []
        self.reward_timer = 0
        self.last_reward_collision_timer = 0
        self.missed_reward_penalty = 5000
        self.reward_move_interval = 10000
        
    def init_rewards(self):
        self.rewards = [Reward() for _ in range(5)]
        self.reward_timer = pygame.time.get_ticks()
        self.last_reward_collision_timer = pygame.time.get_ticks()
        
    def move_rewards(self):
        for reward in self.rewards:
            reward.x = random.randint(100, SCREEN_WIDTH - 130)
            reward.y = random.randint(100, SCREEN_HEIGHT // 2)
            reward.size = random.randint(20, 40)
            reward.type = random.choice(["score", "paddle_extend", "extra_ball"])
            reward.active = True
            
    def check_rewards(self, balls, score, paddle):
        current_time = pygame.time.get_ticks()
        if current_time - self.reward_timer >= self.reward_move_interval:
            self.move_rewards()
            self.reward_timer = current_time
            
        if current_time - self.last_reward_collision_timer >= self.missed_reward_penalty:
            score -= 10
            self.last_reward_collision_timer = current_time
            
        for ball in balls:
            for reward in self.rewards:
                if check_reward_collision(ball, reward):
                    self.last_reward_collision_timer = current_time
                    reward.active = False
                    self.apply_reward(reward, score, paddle)
                    
    def apply_reward(self, reward, score, paddle):
        if reward.type == "score":
            score += 25
        elif reward.type == "paddle_extend":
            paddle.width += 30
        elif reward.type == "extra_ball":
            balls.append(Ball())
