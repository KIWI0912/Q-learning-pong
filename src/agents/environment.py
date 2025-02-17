import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bouncing Ball Game")

# Colors
BACKGROUND_COLOR = (255, 209, 220)  # Light pink
BALL_COLOR = (255, 105, 180)        # Hot pink
PADDLE_COLOR = (255, 182, 193)      # Light pink
TEXT_COLOR = (255, 20, 147)         # Deep pink
REWARD_COLOR = (255, 255, 0)        # Yellow

# Game objects
paddle = {
    "x": SCREEN_WIDTH // 2 - 50,
    "width": 100,
    "height": 10,
    "speed": 7
}

balls = []
rewards = []

# Game variables
score = 0
reward_timer = 0
reward_move_interval = 8000
time_elapsed = 0
game_timer = 60
running = True
current_screen = "menu"

# Fonts
font = pygame.font.SysFont("Arial", 36)
small_font = pygame.font.SysFont("Arial", 24)

def init_ball():
    return {
        "x": random.randint(100, SCREEN_WIDTH - 100),
        "y": 50,
        "vx": random.choice([-4, -3, 3, 4]),
        "vy": random.choice([3, 4, 5]),
        "radius": 10
    }

def init_reward():
    return {
        "x": random.randint(50, SCREEN_WIDTH - 50),
        "y": random.randint(50, SCREEN_HEIGHT // 2),
        "radius": 15,
        "active": True,
        "points": random.choice([10, 20, 30])
    }

def draw_star(surface, x, y, radius, color):
    points = []
    for i in range(10):
        angle = i * (2 * np.pi / 10) - np.pi / 2
        r = radius if i % 2 == 0 else radius / 2
        points.append((x + r * np.cos(angle), y + r * np.sin(angle)))
    pygame.draw.polygon(surface, color, points)

def move_rewards():
    for reward in rewards:
        reward["x"] = random.randint(50, SCREEN_WIDTH - 50)
        reward["y"] = random.randint(50, SCREEN_HEIGHT // 2)
        reward["active"] = True

def check_collision(ball, paddle):
    if ball["y"] + ball["radius"] >= SCREEN_HEIGHT - 20:
        if paddle["x"] <= ball["x"] <= paddle["x"] + paddle["width"]:
            return True
    return False

def check_reward_collision(ball, reward):
    if reward["active"]:
        distance = ((ball["x"] - reward["x"]) ** 2 + (ball["y"] - reward["y"]) ** 2) ** 0.5
        if distance < ball["radius"] + reward["radius"]:
            return True
    return False

def draw_menu():
    screen.fill(BACKGROUND_COLOR)
    title = font.render("Bouncing Ball Game", True, TEXT_COLOR)
    start_text = small_font.render("Press ENTER to Start", True, TEXT_COLOR)
    exit_text = small_font.render("Press ESC to Exit", True, TEXT_COLOR)
    controls_text = small_font.render("Use LEFT and RIGHT arrows to move", True, TEXT_COLOR)
    
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 300))
    screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, 350))
    screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, 400))

def init_game():
    global score, balls, rewards, game_timer
    score = 0
    balls = [init_ball()]
    rewards = [init_reward() for _ in range(3)]
    game_timer = 60
    paddle["x"] = SCREEN_WIDTH // 2 - paddle["width"] // 2

def main():
    global running, current_screen, score, game_timer, reward_timer, time_elapsed
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN and current_screen == "menu":
                    current_screen = "game"
                    init_game()

        if current_screen == "menu":
            draw_menu()
        elif current_screen == "game":
            # Handle paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and paddle["x"] > 0:
                paddle["x"] -= paddle["speed"]
            if keys[pygame.K_RIGHT] and paddle["x"] + paddle["width"] < SCREEN_WIDTH:
                paddle["x"] += paddle["speed"]

            # Update game state
            dt = clock.tick(60)
            time_elapsed += dt
            game_timer -= dt / 1000

            # Move rewards periodically
            reward_timer += dt
            if reward_timer >= reward_move_interval:
                move_rewards()
                reward_timer = 0

            # Update balls
            for ball in balls:
                ball["x"] += ball["vx"]
                ball["y"] += ball["vy"]

                # Wall collisions
                if ball["x"] - ball["radius"] <= 0 or ball["x"] + ball["radius"] >= SCREEN_WIDTH:
                    ball["vx"] *= -1
                if ball["y"] - ball["radius"] <= 0:
                    ball["vy"] *= -1

                # Paddle collision
                if check_collision(ball, paddle):
                    ball["vy"] *= -1
                    relative_intersect = (ball["x"] - (paddle["x"] + paddle["width"]/2)) / (paddle["width"]/2)
                    ball["vx"] = relative_intersect * 5

                # Reward collisions
                for reward in rewards:
                    if check_reward_collision(ball, reward):
                        score += reward["points"]
                        reward["active"] = False

                # Reset ball if it goes below paddle
                if ball["y"] > SCREEN_HEIGHT:
                    ball["x"] = random.randint(100, SCREEN_WIDTH - 100)
                    ball["y"] = 50
                    ball["vx"] = random.choice([-4, -3, 3, 4])
                    ball["vy"] = random.choice([3, 4, 5])

            # Draw game state
            screen.fill(BACKGROUND_COLOR)
            
            # Draw paddle
            pygame.draw.rect(screen, PADDLE_COLOR, 
                           (paddle["x"], SCREEN_HEIGHT - 20, 
                            paddle["width"], paddle["height"]))
            
            # Draw balls
            for ball in balls:
                pygame.draw.circle(screen, BALL_COLOR, 
                                 (int(ball["x"]), int(ball["y"])), 
                                 ball["radius"])
            
            # Draw rewards
            for reward in rewards:
                if reward["active"]:
                    draw_star(screen, reward["x"], reward["y"], 
                            reward["radius"], REWARD_COLOR)
            
            # Draw score and timer
            score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
            timer_text = font.render(f"Time: {int(game_timer)}", True, TEXT_COLOR)
            screen.blit(score_text, (10, 10))
            screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

            # Check if game is over
            if game_timer <= 0:
                current_screen = "menu"

        pygame.display.flip()

if __name__ == "__main__":
    main()
