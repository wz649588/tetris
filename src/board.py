class Board:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]

    def draw(self, current_tetromino=None):
        display = [row[:] for row in self.board]
        if current_tetromino:
            shape = current_tetromino.get_shape()
            x, y = current_tetromino.position
            for i, row in enumerate(shape):
                for j, cell in enumerate(row):
                    if cell:
                        xi, yj = x + i, y + j
                        if 0 <= xi < self.height and 0 <= yj < self.width:
                            display[xi][yj] = 2  # Use 2 for active tetromino
        for row in display:
            print(''.join(['#' if cell == 1 else ('*' if cell == 2 else '.') for cell in row]))
        print('-' * self.width)

    def clear_lines(self):
        new_board = [row for row in self.board if not all(row)]
        lines_cleared = self.height - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [0 for _ in range(self.width)])
        self.board = new_board
        return lines_cleared

    def is_full(self):
        return any(self.board[0])