class Board:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]

    def clear_lines(self):
        """
        Remove all filled lines from the board, add empty lines at the top,
        and return the number of lines cleared.
        """
        new_board = [row for row in self.board if not all(row)]
        lines_cleared = self.height - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [0 for _ in range(self.width)])
        self.board = new_board
        return lines_cleared

    def is_full(self):
        """
        Return True if the top row has any filled cells (game over condition).
        """
        return any(self.board[0])
