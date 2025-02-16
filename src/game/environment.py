import pygame
import random

class GameEnvironment:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.ball_pos = [self.screen_width // 2, self.screen_height // 2]
        self.ball_vel = [random.choice([-1, 1]), random.choice([-1, 1])]
        self.paddle_pos = [self.screen_width // 2, self.screen_height - 50]
        self.paddle_width = 100
        self.score = 0

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Q-Learning Bouncing Ball Game")

    def reset(self):
        self.ball_pos = [self.screen_width // 2, self.screen_height // 2]
        self.ball_vel = [random.choice([-1, 1]), random.choice([-1, 1])]
        self.paddle_pos = [self.screen_width // 2, self.screen_height - 50]
        self.score = 0

    def step(self, action):
        # Update paddle position based on action
        if action == 0:  # Move left
            self.paddle_pos[0] -= 10
        elif action == 1:  # Move right
            self.paddle_pos[0] += 10

        # Ensure paddle stays within bounds
        self.paddle_pos[0] = max(0, min(self.screen_width - self.paddle_width, self.paddle_pos[0]))

        # Update ball position
        self.ball_pos[0] += self.ball_vel[0]
        self.ball_pos[1] += self.ball_vel[1]

        # Ball collision with walls
        if self.ball_pos[0] <= 0 or self.ball_pos[0] >= self.screen_width:
            self.ball_vel[0] *= -1
        if self.ball_pos[1] <= 0:
            self.ball_vel[1] *= -1

        # Ball collision with paddle
        if (self.paddle_pos[0] < self.ball_pos[0] < self.paddle_pos[0] + self.paddle_width and
                self.ball_pos[1] >= self.screen_height - 50):
            self.ball_vel[1] *= -1
            self.score += 1

        # Check if ball falls below the paddle
        if self.ball_pos[1] > self.screen_height:
            return True  # Game over

        return False  # Continue game

    def render(self):
        self.screen.fill((255, 209, 220))  # Background color
        pygame.draw.rect(self.screen, (255, 182, 193), (self.paddle_pos[0], self.screen_height - 50, self.paddle_width, 10))
        pygame.draw.circle(self.screen, (255, 105, 180), (int(self.ball_pos[0]), int(self.ball_pos[1])), 10)
        pygame.display.flip()
