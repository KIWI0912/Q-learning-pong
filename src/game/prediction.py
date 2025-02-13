def predict_all_balls_landing(balls):
    predictions = []
    for ball in balls:
        if ball.vy > 0:
            time_to_paddle = (SCREEN_HEIGHT - ball.radius - ball.y) / ball.vy
            predicted_x = ball.x + (ball.vx * time_to_paddle)
            
            while predicted_x < 0 or predicted_x > SCREEN_WIDTH:
                if predicted_x < 0:
                    predicted_x = -predicted_x
                if predicted_x > SCREEN_WIDTH:
                    predicted_x = 2 * SCREEN_WIDTH - predicted_x
                    
            predictions.append({
                "x": predicted_x,
                "time": time_to_paddle,
                "ball": ball
            })
            
    predictions.sort(key=lambda p: p["time"])
    return predictions

def calculate_reward(balls, paddle, action):
    reward = 0
    predictions = predict_all_balls_landing(balls)
    
    if not predictions:
        return 0
        
    paddle_center = paddle.x + paddle.width / 2
    
    for i, pred in enumerate(predictions):
        weight = 1.0 / (i + 1)
        distance_to_prediction = abs(pred["x"] - paddle_center)
        
        if pred["x"] > paddle_center and action == 1:
            reward += 2 * weight
        elif pred["x"] < paddle_center and action == -1:
            reward += 2 * weight
        elif abs(pred["x"] - paddle_center) < paddle.width/2 and action == 0:
            reward += 3 * weight
            
        if distance_to_prediction < paddle.width:
            reward += (paddle.width - distance_to_prediction) / paddle.width * 5 * weight
        elif distance_to_prediction > paddle.width * 1.5:
            reward -= 3 * weight
            
    return reward
