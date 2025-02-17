# User Manual  

## 🛠️ Installation Guide  
1. **Clone Repository**  
   ```bash
   git clone https://github.com/KIWI0912/q-learning-pong.git
   cd q-learning-pong
   ```

2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Controls  
### Game Interface  
| Key          | Function                  |
|--------------|---------------------------|
| `Enter`      | Start game                |
| `R`          | Return to menu            |
| `Esc`        | Quit game                 |


**Q: Why is the AI unstable?**  
- Try reducing learning rate (`LEARNING_RATE < 0.5`)
- Increase training episodes (`EPISODES > 1000`)
