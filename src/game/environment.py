# src/game/environment.py

import pygame
import random
import numpy as np
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
        
        # 游戏状态
        self.clock = pygame.time.Clock()
        self.mode = mode
        self.reset_game()
        
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
        return self.get_state()
        
    def init_ball(self):
        """初始化球"""
        return {
            "x": random.randint(100, self.SCREEN_WIDTH - 100),
            "y": 50,
            "vx": random.choice([-4, -3, 3, 4]),
            "vy": random.choice([3, 4, 5]),
            "radius": 10
        }
        
    # ... [其他方法保持不变，但移动到类内部]

    def run(self):
        """主游戏循环"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["auto", "manual"], default="auto")
    args = parser.parse_args()
    
    game = PongGame(mode=args.mode)
    game.run()

if __name__ == "__main__":
    main()
