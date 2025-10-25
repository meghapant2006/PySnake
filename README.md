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

2. **Install dependencies** (if running manually):
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

The project includes a configured virtual environment. If you want to set up your own:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install pygame numpy

# Run the game
python snake_game.py
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

## Game Mechanics 🎯

### Scoring
- **+10 points** for each food item consumed
- Score and snake length displayed in real-time
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
├── snake_game.py      # Main game file with all core logic
├── sound_manager.py   # Sound effects management
├── run_game.bat      # Windows launcher script
├── README.md         # This file
├── .venv/           # Virtual environment (auto-generated)
└── requirements.txt  # Dependencies (if needed)
```

## Customization 🎨

### Colors
Modify the `Colors` class in `snake_game.py` to change the color scheme:
```python
class Colors:
    BACKGROUND = (15, 15, 35)      # Dark navy background
    SNAKE_HEAD = (100, 255, 100)   # Bright green head
    FOOD = (255, 100, 100)         # Bright red food
    # ... etc
```

### Game Speed
Change the FPS in the main game loop:
```python
self.clock.tick(10)  # Higher number = faster game
```

### Grid Size
Modify the grid size constants:
```python
GRID_SIZE = 20  # Pixel size of each grid cell
```

## Troubleshooting 🛠️

### Common Issues

1. **"pygame not found"**
   - Solution: Install pygame with `pip install pygame`

2. **"numpy not found"** 
   - Solution: Install numpy with `pip install numpy`

3. **No sound effects**
   - The game will work without sound if numpy/pygame.mixer fails
   - Check that your system supports audio output

4. **Game window doesn't open**
   - Ensure you have a display/monitor connected
   - Try running from command line to see error messages

### Performance Issues
- Close other applications to free up system resources
- Lower the FPS if the game runs too fast on your system
- Ensure your Python installation is up to date

## Development 👩‍💻

### Code Style
- Follows PEP 8 Python style guidelines
- Type hints for better code documentation
- Modular design for easy maintenance and extension

### Extending the Game
The code is designed to be easily extensible:
- Add new sound effects in `sound_manager.py`
- Modify visual effects in the draw methods
- Add new game modes by extending the `SnakeGame` class
- Implement high score tracking
- Add power-ups or special food types

## License 📄

This project is open source and available under the MIT License.

## Credits 🙏

- Built with [Pygame](https://pygame.org/) - Python game development library
- Sound generation using [NumPy](https://numpy.org/) - Numerical computing library
- Inspired by the classic Snake game

---

**Enjoy playing PySnake!** 🐍✨

If you encounter any issues or have suggestions for improvements, feel free to create an issue or contribute to the project.