from tetris.board import Board


def test_clear_lines():
    board = Board(width=4, height=4)
    board.board = [[1, 1, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1], [0, 0, 0, 0]]
    cleared = board.clear_lines()
    assert cleared == 2
    assert board.board[0] == [0, 0, 0, 0]  # New empty row at top


def test_is_full_true_false():
    board = Board(width=4, height=4)
    board.board[0] = [1, 0, 0, 0]
    assert board.is_full()
    board.board[0] = [0, 0, 0, 0]
    assert not board.is_full()
