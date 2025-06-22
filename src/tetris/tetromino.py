"""
tetromino.py

Defines the Tetromino shapes and the Tetromino class for the Tetris game.

- TETROMINO_SHAPES: Dictionary mapping shape names ('I', 'O', 'T', 'S', 'Z', 'J', 'L')
  to their rotation states, represented as 2D lists.
- Tetromino class: Represents a tetromino piece, including its shape, position,
  rotation, and optional name.

Class Overview:
---------------
Tetromino:
    - __init__: Initializes a tetromino with a shape, position, rotation, and optional name.
    - rotate: Rotates the tetromino to the next rotation state.
    - move(dx, dy): Moves the tetromino by (dx, dy) on the board.
    - get_shape: Returns the current rotation's shape matrix.

Usage:
------
- Used by the Game class to manage the active and upcoming tetrominoes.
- The shape and rotation logic is handled here, while placement and collision
  are managed by the Board and Game classes.
"""

TETROMINO_SHAPES = {
    'I': [
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]]
    ],
    'O': [
        [[1, 1],
         [1, 1]]
    ],
    'T': [
        [[0, 1, 0],
         [1, 1, 1]],
        [[1, 0],
         [1, 1],
         [1, 0]],
        [[1, 1, 1],
         [0, 1, 0]],
        [[0, 1],
         [1, 1],
         [0, 1]]
    ],
    'S': [
        [[0, 1, 1],
         [1, 1, 0]],
        [[1, 0],
         [1, 1],
         [0, 1]]
    ],
    'Z': [
        [[1, 1, 0],
         [0, 1, 1]],
        [[0, 1],
         [1, 1],
         [1, 0]]
    ],
    'J': [
        [[1, 0, 0],
         [1, 1, 1]],
        [[1, 1],
         [1, 0],
         [1, 0]],
        [[1, 1, 1],
         [0, 0, 1]],
        [[0, 1],
         [0, 1],
         [1, 1]]
    ],
    'L': [
        [[0, 0, 1],
         [1, 1, 1]],
        [[1, 0],
         [1, 0],
         [1, 1]],
        [[1, 1, 1],
         [1, 0, 0]],
        [[1, 1],
         [0, 1],
         [0, 1]]
    ]
}

class Tetromino:
    """
    Represents a tetromino piece in the Tetris game.

    Attributes:
        shape: List of rotation states (each a 2D list).
        position: [row, col] position on the board.
        rotation: Current rotation index.
        shape_name: Optional name of the shape ('I', 'O', etc.).
    """
    def __init__(self, shape, position, rotation=0, shape_name=None):
        self.shape = shape
        self.position = position
        self.rotation = rotation
        self.shape_name = shape_name  # Store the name if needed

    def rotate(self):
        """Rotate the tetromino to the next rotation state."""
        self.rotation = (self.rotation + 1) % len(self.shape)

    def move(self, dx, dy):
        """Move the tetromino by (dx, dy) on the board."""
        self.position[0] += dx
        self.position[1] += dy

    def get_shape(self):
        """Return the current rotation's shape matrix."""
        return self.shape[self.rotation % len(self.shape)]