# Q-learning-pong

A Python implementation of the classic Pong game with Q-Learning AI, designed for educational and research purposes.

## Features
- **Q-Learning AI**: Implements a reinforcement learning agent to control the paddle.
- **Customizable Game**: Easily adjust game parameters like paddle size, ball speed, and more.
- **Real-time Visualization**: Watch the AI learn and improve in real-time.
- **Performance Analytics**: Track and analyze the AI's learning progress.
- **Modular Design**: Well-structured codebase for easy extension and experimentation.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/KIWI0912/Q-learning-pong.git
   cd Q-learning-pong
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:
   ```bash
   python -m src.game.environment
   ```

## Have fun 🎉

### Playing the Game
To play the game manually:
```bash
python -m src.manual.environment
```

## Project Structure

```
q-learning-pong/
├── README.md                # Project overview
├── requirements.txt         # Python dependencies
├── src/                     # Source code
│   ├── game/                # Game logic
│   ├── manual/              # Manual operation
│   └── statistics/          # Count game time and score
└── docs/                    # Documentation
```

## Documentation
- **[Algorithm Documentation](docs/algorithm_doc.md)**: Detailed explanation of the Q-Learning algorithm.
- **[Performance Analysis](docs/performance_analysis.md)**: Analysis of the AI's learning performance.
- **[User Manual](docs/user_manual.md)**: Step-by-step guide to using the project.
  💡If you need to know how to generate statistical tables and pictures, please click on this document💡

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- **Pygame**: For the game engine implementation.
- **NumPy**: For efficient numerical computations.
- **Matplotlib**: For performance visualization.
- **csv**: For create the required excel file
- **OpenAI Gym**: For inspiration on environment design.

## Contact
For any questions or suggestions, please open an issue or contact the maintainer at [ckiwi912@gmail.com].



Happy coding! 🎮
