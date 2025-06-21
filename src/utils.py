def generate_random_tetromino():
    import random
    shapes = [
        [[1, 1, 1, 1]],  # I
        [[1, 1], [1, 1]],  # O
        [[0, 1, 0], [1, 1, 1]],  # T
        [[1, 1, 0], [0, 1, 1]],  # S
        [[0, 1, 1], [1, 1, 0]],  # Z
        [[1, 0, 0], [1, 1, 1]],  # L
        [[0, 0, 1], [1, 1, 1]],  # J
    ]
    return random.choice(shapes)

def check_collision(board, shape, offset):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board_x = x + offset[0]
                board_y = y + offset[1]
                if board_x < 0 or board_x >= len(board[0]) or board_y >= len(board):
                    return True
                if board_y >= 0 and board[board_y][board_x]:
                    return True
    return False

def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]