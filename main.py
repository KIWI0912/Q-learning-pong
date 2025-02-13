import pygame
from src.game.core import Game
from src.agents.q_learner import QLearning
from src.visualization.renderer import draw_game

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    game = Game()
    agent = QLearning()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                
        if game.balls:
            state = agent.get_state(game.balls, game.paddle)
            action = agent.choose_action(state)
            game.update(action)
            next_state = agent.get_state(game.balls, game.paddle)
            reward = calculate_reward(game.balls, game.paddle, action)
            agent.update(state, action, reward, next_state)
            
        draw_game(screen, game.balls, game.paddle, 
                 game.rewards, game.score, game.time_elapsed)
        
        pygame.display.flip()
        clock.tick(60)
