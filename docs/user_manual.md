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

## 🎮 Controls  
### Game Interface  
| Key          | Function                  |
|--------------|---------------------------|
| `Enter`      | Start game/skip intro     |
| `R`          | Reset level               |
| `Esc`        | Quit game                 |
| `F1`         | Toggle debug info         |


**Q: Why is the AI unstable?**  
- Try reducing learning rate (`LEARNING_RATE < 0.5`)
- Increase training episodes (`EPISODES > 1000`)
