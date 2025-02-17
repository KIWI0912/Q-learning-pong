import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Manual Control Bouncing Ball Game")

# Colors
BACKGROUND_COLOR = (255, 209, 220)  # Light pink
BALL_COLOR = (255, 105, 180)        # Hot pink
PADDLE_COLOR = (255, 182, 193)      # Light pink
TEXT_COLOR = (255, 20, 147)         # Deep pink
REWARD_COLOR = (255, 255, 0)        # Yellow for rewards

# Fonts
font = pygame.font.SysFont("Arial", 36)
small_font = pygame.font.SysFont("Arial", 24)

# Game variables
clock = pygame.time.Clock()
running = True
current_screen = "menu"
score = 0
balls = []
paddle = {}
rewards = []
reward_timer = 0
reward_move_interval = 10000  # Rewards change every 10 seconds (in milliseconds)
time_elapsed = 0
game_timer = 60  # Countdown timer in seconds
INITIAL_PADDLE_WIDTH = 100

# New variables for reward collision penalty
last_reward_collision_timer = 0
missed_reward_penalty = 5000

def init_ball():
    return {
        "x": random.randint(100, SCREEN_WIDTH - 100), 
        "y": 50, 
        "vx": random.choice([-4, -3, 3, 4]), 
        "vy": random.choice([3, 4, 5]), 
        "radius": 10
    }

def init_paddle():
    return {"x": SCREEN_WIDTH // 2 - 50, "width": INITIAL_PADDLE_WIDTH, "height": 10, "speed": 5}

def init_reward():
    return {
        "x": random.randint(100, SCREEN_WIDTH - 130),
        "y": random.randint(100, SCREEN_HEIGHT // 2),
        "size": random.randint(20, 40),
        "active": True,
        "type": random.choice(["score", "paddle_extend", "extra_ball"])
    }

def draw_star(surface, x, y, size, color):
    points = []
    for i in range(10):
        angle = i * (360 / 10) - 90
        radius = size if i % 2 == 0 else size // 2
        x_point = x + radius * np.cos(np.radians(angle))
        y_point = y + radius * np.sin(np.radians(angle))
        points.append((x_point, y_point))
    pygame.draw.polygon(surface, color, points)

def move_rewards():
    for reward in rewards:
        reward["x"] = random.randint(100, SCREEN_WIDTH - 130)
        reward["y"] = random.randint(100, SCREEN_HEIGHT // 2)
        reward["size"] = random.randint(20, 40)
        reward["type"] = random.choice(["score", "paddle_extend", "extra_ball"])
        reward["active"] = True

def ball_reward_collision(ball, reward):
    if reward["active"] and reward["x"] <= ball["x"] <= reward["x"] + reward["size"] and \
       reward["y"] <= ball["y"] <= reward["y"] + reward["size"]:
        reward["active"] = False
        return reward["type"]
    return None

def draw_game():
    screen.fill(BACKGROUND_COLOR)
    
    for ball in balls:
        pygame.draw.circle(screen, BALL_COLOR, (int(ball["x"]), int(ball["y"])), ball["radius"])
    
    pygame.draw.rect(screen, PADDLE_COLOR, (int(paddle["x"]), SCREEN_HEIGHT - paddle["height"], 
                                          paddle["width"], paddle["height"]))
    
    for reward in rewards:
        if reward["active"]:
            draw_star(screen, reward["x"] + reward["size"] // 2, 
                     reward["y"] + reward["size"] // 2, reward["size"] // 2, REWARD_COLOR)
    
    score_text = small_font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))
    
    timer_text = small_font.render(f"Time: {int(game_timer - time_elapsed)}", True, TEXT_COLOR)
    screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if current_screen == "menu":
        screen.fill(BACKGROUND_COLOR)
        title = font.render("Manual Control Bouncing Ball Game", True, TEXT_COLOR)
        start_text = small_font.render("Press ENTER to Start", True, TEXT_COLOR)
        exit_text = small_font.render("Press ESC to Exit", True, TEXT_COLOR)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 300))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, 350))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            current_screen = "game"
            score = 0
            balls = [init_ball()]
            paddle = init_paddle()
            rewards = [init_reward() for _ in range(10)]
            time_elapsed = 0
            reward_timer = pygame.time.get_ticks()
            last_reward_collision_timer = pygame.time.get_ticks()
        elif keys[pygame.K_ESCAPE]:
            running = False

    elif current_screen == "game":
        if not balls:
            balls = [init_ball()]

        # Manual control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle["x"] > 0:
            paddle["x"] -= paddle["speed"]
        if keys[pygame.K_RIGHT] and paddle["x"] + paddle["width"] < SCREEN_WIDTH:
            paddle["x"] += paddle["speed"]

        for ball in balls[:]:
            ball["x"] += ball["vx"]
            ball["y"] += ball["vy"]

            if ball["x"] <= 0 or ball["x"] >= SCREEN_WIDTH:
                ball["vx"] = -ball["vx"]
            if ball["y"] <= 0:
                ball["vy"] = -ball["vy"]
            if ball["y"] >= SCREEN_HEIGHT:
                balls.remove(ball)
                if len(balls) == 0:
                    score -= 10
                    balls.append(init_ball())

            if paddle["x"] <= ball["x"] <= paddle["x"] + paddle["width"] and \
               ball["y"] + ball["radius"] >= SCREEN_HEIGHT - paddle["height"]:
                ball["vy"] = -abs(ball["vy"])
                score += 5

            for reward in rewards:
                reward_type = ball_reward_collision(ball, reward)
                if reward_type:
                    last_reward_collision_timer = pygame.time.get_ticks()
                    if reward_type == "score":
                        score += 25
                    elif reward_type == "paddle_extend":
                        paddle["width"] += 30
                    elif reward_type == "extra_ball":
                        balls.append(init_ball())

        if pygame.time.get_ticks() - last_reward_collision_timer >= missed_reward_penalty:
            score -= 10
            last_reward_collision_timer = pygame.time.get_ticks()

        if pygame.time.get_ticks() - reward_timer >= reward_move_interval:
            move_rewards()
            reward_timer = pygame.time.get_ticks()

        draw_game()

        time_elapsed += clock.get_time() / 1000
        if time_elapsed >= game_timer:
            current_screen = "end_screen"

    elif current_screen == "end_screen":
        screen.fill(BACKGROUND_COLOR)
        end_text = font.render("Time's Up!", True, TEXT_COLOR)
        score_text = small_font.render(f"Your Score: {score}", True, TEXT_COLOR)
        menu_text = small_font.render("Press R to Return to Menu", True, TEXT_COLOR)
        exit_text = small_font.render("Press ESC to Exit", True, TEXT_COLOR)
        
        screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, 200))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 400))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, 450))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            current_screen = "menu"
        elif keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
