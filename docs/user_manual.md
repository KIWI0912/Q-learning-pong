# User Manual  

## 🛠️ Installation Guide  
1. **Clone Repository**  
   ```bash
   git clone https://github.com/YOURNAME/q-learning-paddle-game.git
   cd q-learning-paddle-game
   ```

2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch Game**  
   ```bash
   python main.py --train  # Training mode
   python main.py --play   # Play mode
   ```

## 🎮 Controls  
### Game Interface  
| Key          | Function                  |
|--------------|---------------------------|
| `Enter`      | Start game/skip intro     |
| `R`          | Reset level               |
| `Esc`        | Quit game                 |
| `F1`         | Toggle debug info         |

### Configuration  
Edit `config.py` to customize:  
```python
# Q-Learning Parameters
LEARNING_RATE = 0.7    # Learning rate (0~1)
DISCOUNT_FACTOR = 0.9  # Discount factor (0~1)

# Game Parameters
MAX_STEPS = 3000       # Max steps per episode
PENALTY_IDLE = -0.1    # Penalty for staying idle
REWARD_HIT = +1.5      # Reward for successful hit
```

## ❓ FAQ  
**Q: How to save training results?**  
```bash
python main.py --train --save_model q_table.pkl
```

**Q: Why is the AI unstable?**  
- Try reducing learning rate (`LEARNING_RATE < 0.5`)
- Increase training episodes (`EPISODES > 1000`)
