def draw_game(screen, balls, paddle, rewards, score, time_left):
    screen.fill(BACKGROUND_COLOR)
    
    # Draw the balls
    for ball in balls:
        pygame.draw.circle(screen, BALL_COLOR, 
                          (int(ball.x), int(ball.y)), ball.radius)
    
    # Draw the paddle
    pygame.draw.rect(screen, PADDLE_COLOR, 
                    (int(paddle.x), SCREEN_HEIGHT - paddle.height,
                     paddle.width, paddle.height))
    
    # Draw the reward
    for reward in rewards:
        if reward.active:
            draw_star(screen, reward.x + reward.size // 2,
                     reward.y + reward.size // 2, 
                     reward.size // 2, REWARD_COLOR)
    
    # Draw the score and time
    score_text = small_font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))
    
    timer_text = small_font.render(f"Time: {int(time_left)}", True, TEXT_COLOR)
    screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))
