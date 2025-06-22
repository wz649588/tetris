from tetris.tetromino import Tetromino, TETROMINO_SHAPES

def test_rotation():
    shape = TETROMINO_SHAPES['I']
    t = Tetromino(shape, [0, 0])
    assert t.get_shape() == shape[0]
    t.rotate()
    assert t.get_shape() == shape[1]
    t.rotate()
    assert t.get_shape() == shape[0]  # Wraps around

def test_move():
    shape = TETROMINO_SHAPES['O']
    t = Tetromino(shape, [0, 0])
    t.move(1, 2)
    assert t.position == [1, 2]