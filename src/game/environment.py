# src/game/environment.py

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

    def get_state(self):
        """获取当前游戏状态"""
        if not self.balls:
            return None
        
        dangerous_balls = [b for b in self.balls if b["vy"] > 0]
        if not dangerous_balls:
            dangerous_balls = self.balls
        
        closest_ball = min(dangerous_balls, 
                          key=lambda b: (self.SCREEN_HEIGHT - b["y"]) / abs(b["vy"]) if b["vy"] != 0 else float('inf'))
        
        ball_x = int(closest_ball["x"] // 50)
        ball_y = int(closest_ball["y"] // 50)
        ball_direction = 1 if closest_ball["vx"] > 0 else -1
        ball_vertical = 1 if closest_ball["vy"] > 0 else -1
        paddle_x = int(self.paddle["x"] // 50)
        
        return (ball_x, ball_y, paddle_x, ball_direction, ball_vertical)

    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if self.current_screen == "menu":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    self.current_screen = "game"
                elif keys[pygame.K_ESCAPE]:
                    self.running = False
                    
            elif self.current_screen == "end_screen":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.reset_game()
                    self.current_screen = "menu"
                elif keys[pygame.K_ESCAPE]:
                    self.running = False

    def update(self):
        """更新游戏状态"""
        if self.current_screen == "game":
            self.update_game_state()
            self.time_elapsed += self.clock.get_time() / 1000
            if self.time_elapsed >= self.game_timer:
                self.current_screen = "end_screen"

    def update_game_state(self):
        """更新游戏对象状态"""
        # 更新球的位置和碰撞检测
        for ball in self.balls[:]:
            ball["x"] += ball["vx"]
            ball["y"] += ball["vy"]
            
            # 边界碰撞
            if ball["x"] <= 0 or ball["x"] >= self.SCREEN_WIDTH:
                ball["vx"] = -ball["vx"]
            if ball["y"] <= 0:
                ball["vy"] = -ball["vy"]
            if ball["y"] >= self.SCREEN_HEIGHT:
                self.balls.remove(ball)
                if len(self.balls) == 0:
                    self.score -= 10
                    self.balls.append(self.init_ball())
            
            # 挡板碰撞
            if (self.paddle["x"] <= ball["x"] <= self.paddle["x"] + self.paddle["width"] and
                ball["y"] + ball["radius"] >= self.SCREEN_HEIGHT - self.paddle["height"]):
                ball["vy"] = -abs(ball["vy"])
                self.score += 5

    def render(self):
        """渲染游戏画面"""
        self.screen.fill(self.BACKGROUND_COLOR)
        
        if self.current_screen == "menu":
            self.render_menu()
        elif self.current_screen == "game":
            self.render_game()
        elif self.current_screen == "end_screen":
            self.render_end_screen()
            
        pygame.display.flip()

    def render_menu(self):
        """渲染菜单画面"""
        title = self.font.render("Q-Learning Bouncing Ball Game", True, self.TEXT_COLOR)
        start_text = self.small_font.render("Press ENTER to Start", True, self.TEXT_COLOR)
        exit_text = self.small_font.render("Press ESC to Exit", True, self.TEXT_COLOR)
        
        self.screen.blit(title, (self.SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        self.screen.blit(start_text, (self.SCREEN_WIDTH // 2 - start_text.get_width() // 2, 300))
        self.screen.blit(exit_text, (self.SCREEN_WIDTH // 2 - exit_text.get_width() // 2, 350))

    def render_game(self):
        """渲染游戏画面"""
        # 绘制球
        for ball in self.balls:
            pygame.draw.circle(self.screen, self.BALL_COLOR, 
                             (int(ball["x"]), int(ball["y"])), ball["radius"])
        
        # 绘制挡板
        pygame.draw.rect(self.screen, self.PADDLE_COLOR,
                        (int(self.paddle["x"]), 
                         self.SCREEN_HEIGHT - self.paddle["height"],
                         self.paddle["width"], 
                         self.paddle["height"]))
        
        # 绘制分数和时间
        score_text = self.small_font.render(f"Score: {self.score}", True, self.TEXT_COLOR)
        timer_text = self.small_font.render(f"Time: {int(self.game_timer - self.time_elapsed)}", 
                                          True, self.TEXT_COLOR)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(timer_text, (self.SCREEN_WIDTH - 150, 10))

    def render_end_screen(self):
        """渲染结束画面"""
        end_text = self.font.render("Time's Up!", True, self.TEXT_COLOR)
        score_text = self.small_font.render(f"Your Score: {self.score}", True, self.TEXT_COLOR)
        menu_text = self.small_font.render("Press R to Return to Menu", True, self.TEXT_COLOR)
        exit_text = self.small_font.render("Press ESC to Exit", True, self.TEXT_COLOR)
        
        self.screen.blit(end_text, (self.SCREEN_WIDTH // 2 - end_text.get_width() // 2, 200))
        self.screen.blit(score_text, (self.SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
        self.screen.blit(menu_text, (self.SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 400))
        self.screen.blit(exit_text, (self.SCREEN_WIDTH // 2 - exit_text.get_width() // 2, 450))

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["auto", "manual"], default="auto")
    args = parser.parse_args()
    
    game = PongGame(mode=args.mode)
    game.run()

if __name__ == "__main__":
    main()
