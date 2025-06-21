# Tetris Game

A classic Tetris game implemented in Python 3.12 using pygame, featuring:
- Fullscreen graphical UI
- Smooth keyboard controls
- Score and level display
- Next tetromino preview
- Increasing speed with each level
- Flash effect when clearing four lines (Tetris)
- Game over detection

## Requirements

- Python 3.12
- pygame

Install dependencies with:

```
pip install -r requirements.txt
```

## How to Run

1. Clone the repository or download the project files.
2. Make sure you are in the project directory.
3. Run the game with:

```
python src/main.py
```

## Controls

- **Left/Right Arrow:** Move tetromino left/right
- **Down Arrow:** Soft drop (move down faster)
- **Up Arrow:** Rotate tetromino
- **Q:** Quit the game

## Features

- Fullscreen mode with centered board and UI
- Score and level shown at the top
- Next tetromino preview on the right
- Board flashes yellow when you clear four lines at once (Tetris)
- Game speed increases as you level up

## Notes

- The game window will open in fullscreen. Press `Q` to quit.
- Designed for Python 3.12 and tested on Linux.
- Sound effects can be added by placing a `tetris.wav` file in the `src` directory and updating the code to play it when a Tetris is cleared.

Enjoy playing Tetris!