# Algorithm Documentation

## Overview
This document explains the Q-learning algorithm and its implementation in the project.

## Q-Learning Algorithm
Q-learning is a model-free reinforcement learning algorithm. The Q-value is updated using the following formula:

Q(s,a) = Q(s,a) + α * (r + γ * max(Q(s',a')) - Q(s,a))

Where:
- `s`: Current state
- `a`: Current action
- `r`: Immediate reward
- `s'`: Next state
- `α`: Learning rate
- `γ`: Discount factor

## State Representation
The state is represented as a 6-tuple:

(ball_x, ball_y, paddle_x, ball_direction, ball_vertical, other_balls_info)


## Action Space
The action space consists of discrete values:
- `-1`: Move left
- `0`: Stay still
- `1`: Move right
