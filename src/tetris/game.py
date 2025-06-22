"""
game.py

This module contains the Game class, which manages the main Tetris game logic,
including the board state, tetromino queue, scoring, level progression, and
game-over detection. This version is designed for graphical (pygame) play only.

Key Features:
-------------
- Manages the board and active tetromino.
- Maintains a queue of the next two tetrominoes for preview.
- Handles movement, placement, and collision detection.
- Implements scoring and level-up rules.
- Triggers a flash effect when a Tetris (4 lines) is cleared.
- Detects game over when a new tetromino cannot be placed.

Class Overview:
---------------
Game:
    - __init__: Initializes game state, board, tetromino queue, and flash timer.
    - generate_random_tetromino: Returns a new random Tetromino object.
    - spawn_new_tetromino: Moves the next tetromino from the queue to active, checks for game over.
    - can_move(dx, dy): Checks if the current tetromino can move by (dx, dy).
    - place_tetromino: Locks the current tetromino, clears lines, updates score/level, and spawns the next.
    - update: Advances the game state (gravity).
    - increase_score: Adds points to the score.
    - stop: Ends the game.

Usage:
------
- The Game class is intended to be used by a graphical frontend (e.g., pygame).
- The frontend should call Game methods to move, rotate, and place tetrominoes,
  and use Game attributes to display the board, score, level, and next pieces.

Example:
--------
    game = Game()
    while game.is_running:
        # Handle input, call game.can_move(), game.place_tetromino(), etc.
        # Draw the board and UI using game.board, game.current_tetromino, game.next_tetrominoes, etc.
"""

import random
from tetris.tetromino import TETROMINO_SHAPES, Tetromino
from tetris.board import Board

class Game:
    def __init__(self):
        """
        Initialize the game state, including score, level, board, and tetromino queue.
        """
        self.score = 0
        self.level = 1
        self.lines_cleared_total = 0
        self.is_running = True
        self.board = Board()
        self.current_tetromino = None
        # Initialize a queue of 2 next tetrominoes for preview
        self.next_tetrominoes = [self.generate_random_tetromino() for _ in range(2)]
        self.spawn_new_tetromino()
        self.flash_timer = 0

    def generate_random_tetromino(self):
        """
        Generate a new random Tetromino object.
        """
        shape_name = random.choice(list(TETROMINO_SHAPES.keys()))
        shape = TETROMINO_SHAPES[shape_name]
        position = [0, (self.board.width - len(shape[0][0])) // 2]
        return Tetromino(shape, position, shape_name=shape_name)

    def spawn_new_tetromino(self):
        """
        Move the next tetromino from the queue to active, and add a new one to the queue.
        Checks for immediate collision (game over).
        """
        self.current_tetromino = self.next_tetrominoes.pop(0)
        self.next_tetrominoes.append(self.generate_random_tetromino())
        # Check for immediate collision (game over)
        shape_matrix = self.current_tetromino.get_shape()
        x, y = self.current_tetromino.position
        for i, row in enumerate(shape_matrix):
            for j, cell in enumerate(row):
                if cell:
                    new_x = x + i
                    new_y = y + j
                    if (new_x < 0 or new_x >= self.board.height or
                        new_y < 0 or new_y >= self.board.width or
                        self.board.board[new_x][new_y]):
                        self.is_running = False
                        print("Game Over!")
                        return

    def can_move(self, dx, dy):
        """
        Check if the current tetromino can move by (dx, dy).
        Returns True if the move is valid, False otherwise.
        """
        shape = self.current_tetromino.get_shape()
        x, y = self.current_tetromino.position
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = x + i + dx
                    new_y = y + j + dy
                    if (new_x < 0 or new_x >= self.board.height or
                        new_y < 0 or new_y >= self.board.width or
                        self.board.board[new_x][new_y]):
                        return False
        return True

    def place_tetromino(self):
        """
        Lock the current tetromino in place, clear lines, update score and level,
        trigger flash effect if needed, and spawn the next tetromino.
        """
        shape = self.current_tetromino.get_shape()
        x, y = self.current_tetromino.position
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    self.board.board[x + i][y + j] = 1
        lines_cleared = self.board.clear_lines()
        self.lines_cleared_last = lines_cleared
        self.lines_cleared_total += lines_cleared  # Track total lines
        if lines_cleared == 4:
            self.flash_timer = 10  # Number of frames to flash
        if lines_cleared > 0:
            if lines_cleared == 1:
                self.increase_score(100)
            elif lines_cleared == 2:
                self.increase_score(300)
            elif lines_cleared == 3:
                self.increase_score(500)
            elif lines_cleared == 4:
                self.increase_score(800)
        # Level up every 10 lines
        if self.lines_cleared_total // 10 + 1 > self.level:
            self.level += 1
        self.spawn_new_tetromino()

    def update(self):
        """
        Advance the game state by one step (gravity).
        """
        if self.current_tetromino:
            if self.can_move(1, 0):
                self.current_tetromino.move(1, 0)
            else:
                self.place_tetromino()

    def increase_score(self, points):
        """
        Add points to the current score.
        """
        self.score += points

    def stop(self):
        """
        End the game.
        """
        self.is_running = False