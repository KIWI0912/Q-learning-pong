class Ball:
    def __init__(self):
        self.x = random.randint(100, SCREEN_WIDTH - 100)
        self.y = 50
        self.vx = random.choice([-4, -3, 3, 4])
        self.vy = random.choice([3, 4, 5])
        self.radius = 10

class Paddle:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - 50
        self.width = INITIAL_PADDLE_WIDTH
        self.height = 10
        self.speed = 5

class Reward:
    def __init__(self):
        self.x = random.randint(100, SCREEN_WIDTH - 130)
        self.y = random.randint(100, SCREEN_HEIGHT // 2)
        self.size = random.randint(20, 40)
        self.active = True
        self.type = random.choice(["score", "paddle_extend", "extra_ball"])
