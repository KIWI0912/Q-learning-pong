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
   
3. **Run the game have statistical function**
   ```bash
   python -m src.statistical.withcalculate
   ```
   💡Before you run this code, please to change the file path💡
   
5. **Generate statistical pictures and data**
   ```bash
   python -m src.statistical.pyplot
   ```
   💡Before you run this code, please to change the file path💡

   
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
