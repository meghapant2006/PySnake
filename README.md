# PySnake - Classic Snake Game 🐍

A modern, classic Snake game built with Python and Pygame featuring smooth graphics, sound effects, and polished gameplay.

## Features ✨

- **Modern Visual Design**: Sleek dark theme with gradient colors and smooth animations
- **Attractive Graphics**: 
  - Snake with gradient body segments and animated eyes
  - Glowing, pulsating food with smooth animations
  - Grid-based layout with subtle visual effects
  - Professional UI with score and length display
- **Sound Effects**: 
  - Pleasant eating sound when collecting food
  - Game over sound effect
  - Procedurally generated audio using numpy
- **Smooth Gameplay**:
  - Classic snake mechanics with modern polish
  - Collision detection for walls and self-collision
  - Responsive controls (WASD or Arrow keys)
  - Pause functionality
- **Game Features**:
  - High score tracking (session-based)
  - Snake length display
  - Game over screen with restart option
  - Professional game loop and state management

## Controls 🎮

- **Movement**: Use `WASD` keys or `Arrow Keys` to control the snake
- **Pause**: Press `SPACE` to pause/unpause the game
- **Restart**: When game over, press `SPACE` to play again
- **Exit**: Press `ESC` to exit the game

## Installation & Setup 💻

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Start

1. **Clone or download** this project to your local machine

2. **Install dependencies**:
   ```bash
   pip install pygame numpy
   ```

3. **Run the game**:
   
   **Option A**: Use the launcher script (Windows)
   ```bash
   run_game.bat
   ```
   
   **Option B**: Run directly with Python
   ```bash
   python snake_game.py
   ```

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python snake_game.py
```

## Game Mechanics 🎯

### Scoring
- **+10 points** for each food item consumed
- Score and snake length displayed in real-time
- High score tracking during session
- Final score shown on game over screen

### Difficulty
- **Classic Speed**: 10 FPS for traditional snake game feel
- **Progressive Challenge**: Snake gets longer with each food item
- **Collision System**: Game ends on wall or self-collision

### Food System
- **Smart Spawning**: Food never spawns on the snake's body
- **Visual Feedback**: Glowing, animated food for better visibility
- **Immediate Response**: Snake grows immediately upon eating

## File Structure 📁

```
PySnake/
├── snake_game.py          # Main game file with all game logic
├── sound_manager.py       # Sound effects and audio management
├── requirements.txt       # Python dependencies
├── run_game.bat          # Windows launcher script
├── README.md             # This file
└── .venv/               # Virtual environment (auto-created)
```

## Technical Details 🔧

### Architecture
- **Object-Oriented Design**: Clean separation between Snake, Food, and Game classes
- **Modern Python**: Uses type hints, enums, and modern Python practices
- **Modular Code**: Sound manager separated for maintainability
- **Performance Optimized**: Efficient rendering and game loop

### Graphics System
- **Pygame-based**: Reliable cross-platform graphics
- **Grid System**: 20x20 pixel grid for classic snake feel
- **Color Palette**: Carefully chosen modern color scheme
- **Animation**: Smooth animations for food pulsing and visual effects

### Sound System
- **Procedural Audio**: Sound effects generated mathematically using numpy
- **Non-blocking**: Sounds don't interfere with gameplay
- **Graceful Fallback**: Game works even if sound system fails

## Contributing 🤝

Feel free to fork this project and submit pull requests for improvements!

## License 📜

This project is open source and available under the [MIT License](LICENSE).

---

**Enjoy playing PySnake!** 🐍🎮