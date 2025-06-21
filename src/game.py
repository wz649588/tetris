import random
import curses
from tetromino import TETROMINO_SHAPES, Tetromino
from board import Board

class Game:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.lines_cleared_total = 0
        self.is_running = True
        self.board = Board()
        self.current_tetromino = None
        self.next_tetromino = self.generate_random_tetromino()
        self.spawn_new_tetromino()
        self.flash_timer = 0  # Add this line

    def generate_random_tetromino(self):
        shape_name = random.choice(list(TETROMINO_SHAPES.keys()))
        shape = TETROMINO_SHAPES[shape_name]
        position = [0, (self.board.width - len(shape[0][0])) // 2]
        return Tetromino(shape, position, shape_name=shape_name)

    def spawn_new_tetromino(self):
        # Use the next tetromino as the current one
        self.current_tetromino = self.next_tetromino
        # Generate a new next tetromino
        self.next_tetromino = self.generate_random_tetromino()
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

    def start(self):
        self.is_running = True
        curses.wrapper(self.game_loop)

    def game_loop(self, stdscr):
        stdscr.nodelay(True)
        stdscr.timeout(500)  # Slower game speed (ms)
        while self.is_running:
            key = stdscr.getch()
            if key == curses.KEY_LEFT and self.can_move(0, -1):
                self.current_tetromino.move(0, -1)
            elif key == curses.KEY_RIGHT and self.can_move(0, 1):
                self.current_tetromino.move(0, 1)
            elif key == curses.KEY_DOWN and self.can_move(1, 0):
                self.current_tetromino.move(1, 0)
            elif key == curses.KEY_UP:
                # Try to rotate
                old_rotation = self.current_tetromino.rotation
                self.current_tetromino.rotate()
                if not self.can_move(0, 0):
                    self.current_tetromino.rotation = old_rotation
            elif key == ord('q'):
                self.is_running = False

            self.update()
            self.draw_curses(stdscr)

    def draw_curses(self, stdscr):
        stdscr.clear()
        display = [row[:] for row in self.board.board]
        if self.current_tetromino:
            shape = self.current_tetromino.get_shape()
            x, y = self.current_tetromino.position
            for i, row in enumerate(shape):
                for j, cell in enumerate(row):
                    if cell:
                        xi, yj = x + i, y + j
                        if 0 <= xi < self.board.height and 0 <= yj < self.board.width:
                            display[xi][yj] = 2
        for row in display:
            stdscr.addstr(''.join(['#' if cell == 1 else ('*' if cell == 2 else '.') for cell in row]) + '\n')
        stdscr.addstr(f"Score: {self.score}  Level: {self.level}\n")
        stdscr.refresh()

    def update(self):
        if self.current_tetromino:
            if self.can_move(1, 0):
                self.current_tetromino.move(1, 0)
            else:
                self.place_tetromino()

    def increase_score(self, points):
        self.score += points

    def level_up(self):
        self.level += 1

    def stop(self):
        self.is_running = False