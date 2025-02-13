def check_ball_collision(ball, paddle):
    return (paddle.x <= ball.x <= paddle.x + paddle.width and
            ball.y + ball.radius >= SCREEN_HEIGHT - paddle.height)

def check_reward_collision(ball, reward):
    return (reward.active and 
            reward.x <= ball.x <= reward.x + reward.size and
            reward.y <= ball.y <= reward.y + reward.size)
