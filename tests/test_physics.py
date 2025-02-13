import unittest
from src.game.physics import check_ball_collision, check_reward_collision
from src.game.objects import Ball, Paddle, Reward

class TestPhysics(unittest.TestCase):
    def setUp(self):
        self.ball = Ball()
        self.paddle = Paddle()
        self.reward = Reward()
        
    def test_ball_collision(self):
        self.ball.x = self.paddle.x + 10
        self.ball.y = SCREEN_HEIGHT - self.paddle.height - self.ball.radius
        self.assertTrue(check_ball_collision(self.ball, self.paddle))
        
    def test_reward_collision(self):
        self.ball.x = self.reward.x + self.reward.size / 2
        self.ball.y = self.reward.y + self.reward.size / 2
        self.assertTrue(check_reward_collision(self.ball, self.reward))
