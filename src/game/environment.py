# src/game/environment.py

import pygame
import random
import numpy as np
import argparse
import os

class PongGame:
    def __init__(self, mode="auto"):
        pygame.init()
        
        # 基础设置
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Q-Learning Bouncing Ball Game")
        
        # 颜色定义
        self.BACKGROUND_COLOR = (255, 209, 220)
        self.BALL_COLOR = (255, 105, 180)
        self.PADDLE_COLOR = (255, 182, 193)
        self.TEXT_COLOR = (255, 20, 147)
        self.REWARD_COLOR = (255, 255, 0)
        
        # 游戏参数
        self.INITIAL_PADDLE_WIDTH = 100
        self.clock = pygame.time.Clock()
        self.mode = mode
        
        # 初始化字体
        self.font = pygame.font.SysFont("Arial", 36)
        self.small_font = pygame.font.SysFont("Arial", 24)
        
        self.reset_game()

    def init_ball(self):
        """初始化球"""
        return {
            "x": random.randint(100, self.SCREEN_WIDTH - 100),
            "y": 50,
            "vx": random.choice([-4, -3, 3, 4]),
            "vy": random.randint(3, 5),
            "radius": 10
        }

    def init_paddle(self):
        """初始化挡板"""
        return {
            "x": self.SCREEN_WIDTH // 2 - self.INITIAL_PADDLE_WIDTH // 2,
            "width": self.INITIAL_PADDLE_WIDTH,
            "height": 10,
            "speed": 5
        }

    def init_reward(self):
        """初始化奖励"""
        return {
            "x": random.randint(100, self.SCREEN_WIDTH - 130),
            "y": random.randint(100, self.SCREEN_HEIGHT // 2),
            "size": random.randint(20, 40),
            "active": True,
            "type": random.choice(["score", "paddle_extend", "extra_ball"])
        }

    def reset_game(self):
        """重置游戏状态"""
        self.score = 0
        self.balls = [self.init_ball()]
        self.paddle = self.init_paddle()
        self.rewards = [self.init_reward() for _ in range(5)]
        self.time_elapsed = 0
        self.game_timer = 60
        self.running = True
        self.current_screen = "menu"
        self.reward_timer = pygame.time.get_ticks()
        self.last_reward_collision_timer = pygame.time.get_ticks()
        return self.get_state()

    def run(self):
        """运行游戏主循环"""
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.render()
        pygame.quit()

def main():
    parser = argparse.ArgumentParser(description='Pong Game with Q-Learning')
    parser.add_argument('--mode', type=str, default='auto', choices=['auto', 'manual'],
                      help='Game mode: auto (AI) or manual (player)')
    args = parser.parse_args()
    
    game = PongGame(mode=args.mode)
    game.run()

if __name__ == "__main__":
    main()
