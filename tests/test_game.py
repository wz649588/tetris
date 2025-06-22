from tetris.game import Game


def test_spawn_and_move():
    game = Game()
    old_tetromino = game.current_tetromino
    game.spawn_new_tetromino()
    assert game.current_tetromino != old_tetromino


def test_score_and_level():
    game = Game()
    game.lines_cleared_total = 15
    game.place_tetromino()  # Simulate clearing a line
    assert game.level >= 2


def test_can_move():
    game = Game()
    assert game.can_move(0, 0)
