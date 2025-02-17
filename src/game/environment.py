# src/game/environment.py

import pygame
import sys
from ..config.settings import *  # 假设配置在这里

class PongEnvironment:
    def __init__(self, mode="auto"):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Q-Learning Pong")
        self.clock = pygame.time.Clock()
        self.mode = mode
        self.running = True
        
        # 初始化游戏对象
        self.init_game_objects()
        
    def init_game_objects(self):
        # 球和挡板的初始化
        self.paddle_pos = [SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2]
        self.ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.ball_dir = [1, 1]  # 简单的方向向量
        
    def run(self):
        while self.running:
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.mode == "manual":
                    self.handle_manual_input(event)
            
            # 更新游戏状态
            self.update()
            
            # 渲染
            self.render()
            
            # 控制帧率
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def handle_manual_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.paddle_pos[1] -= 10
            elif event.key == pygame.K_DOWN:
                self.paddle_pos[1] += 10
    
    def update(self):
        # 更新球的位置
        self.ball_pos[0] += self.ball_dir[0] * 5
        self.ball_pos[1] += self.ball_dir[1] * 5
        
        # 简单的碰撞检测
        if self.ball_pos[1] <= 0 or self.ball_pos[1] >= SCREEN_HEIGHT:
            self.ball_dir[1] *= -1
        
        # 球和挡板的碰撞
        if (self.ball_pos[0] >= SCREEN_WIDTH - 30 and 
            self.paddle_pos[1] - 50 <= self.ball_pos[1] <= self.paddle_pos[1] + 50):
            self.ball_dir[0] *= -1
        
        # 球出界重置
        if self.ball_pos[0] < 0 or self.ball_pos[0] > SCREEN_WIDTH:
            self.ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    
    def render(self):
        # 清屏
        self.screen.fill((0, 0, 0))
        
        # 绘制挡板
        pygame.draw.rect(self.screen, (255, 255, 255),
                        (self.paddle_pos[0], self.paddle_pos[1] - 50, 10, 100))
        
        # 绘制球
        pygame.draw.circle(self.screen, (255, 255, 255),
                         (int(self.ball_pos[0]), int(self.ball_pos[1])), 5)
        
        # 更新显示
        pygame.display.flip()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["auto", "manual"], default="auto")
    args = parser.parse_args()
    
    # 创建并运行游戏
    env = PongEnvironment(mode=args.mode)
    print(f"Starting game in {args.mode} mode...")
    env.run()

if __name__ == "__main__":
    main()

        self.screen.fill((255, 209, 220))  # Background color
        pygame.draw.rect(self.screen, (255, 182, 193), (self.paddle_pos[0], self.screen_height - 50, self.paddle_width, 10))
        pygame.draw.circle(self.screen, (255, 105, 180), (int(self.ball_pos[0]), int(self.ball_pos[1])), 10)
        pygame.display.flip()
