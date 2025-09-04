# Dodge the Blocks

A simple Python game where you dodge falling blocks. Built with Pygame. Have fun!

## Features

- Player-controlled character
- Randomly spawning falling blocks
- Score tracking
- Virtual environment support
- Easy launcher script
- Modular, well-organized code structure

## Requirements

- [Python 3.x](https://www.python.org/)
- [Pygame 2.6.1](https://www.pygame.org/)

## Installation

### Option 1: Quick Start with Launcher Script (Recommended)

1. Clone or download this repository
2. Run the launcher script:
   ```bash
   ./start_game.sh
   ```

### Option 2: Manual Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the game:
   ```bash
   python main.py
   ```

## How to Play

1. **Launch the game** using one of the methods above
2. **Use LEFT and RIGHT arrow keys** to move your character
3. **Avoid the falling red blocks** - they will end your game
4. **Try to survive as long as possible** and build up your score
5. **After game over:**
   - Press **R** to restart
   - Press **Q** to quit

## Game Controls

- **← →** Arrow Keys: Move left/right
- **R**: Restart game after game over
- **Q**: Quit game after game over

## Project Structure

```
dodge_the_blocks/
├── main.py                 # Main entry point
├── game.py                 # Game controller class
├── player.py               # Player class and logic
├── enemy.py                # Enemy class and logic
├── config.py               # Game configuration and constants
├── start_game.sh           # Launcher script
├── requirements.txt        # Python dependencies
├── venv/                   # Virtual environment (created after setup)
└── README.md               # This file
```

## Development

To work on this project:

1. Activate the virtual environment: `source venv/bin/activate`
2. Make your changes to the appropriate module:
   - `config.py` for game settings
   - `player.py` for player behavior
   - `enemy.py` for enemy behavior
   - `game.py` for game logic
3. Test with: `python main.py`
4. Deactivate when done: `deactivate`

## Code Organization

The game is now organized into logical modules:

- **`config.py`**: Centralized configuration management
- **`player.py`**: Player movement, drawing, and state
- **`enemy.py`**: Enemy behavior and collision detection
- **`game.py`**: Main game loop and coordination
- **`main.py`**: Entry point and pygame initialization

## Troubleshooting

- **"Permission denied" on launcher script**: Run `chmod +x start_game.sh`
- **Virtual environment not found**: Follow the manual setup steps above
- **Pygame not installed**: Make sure to run `pip install -r requirements.txt` in the activated virtual environment
- **Import errors**: Ensure all Python files are in the same directory

## License

MIT License
