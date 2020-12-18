import pytest

from solver import rotate, TETROMINO_SHAPES, TetrominoSolver


@pytest.mark.parametrize(
    "tile,rotation,expected",
    [
        ('I', 1, [['I'], ['I'], ['I'], ['I']]),
        ('I', 2, [['I', 'I', 'I', 'I']]),
        ('O', 1, [['O', 'O'], ['O', 'O']]),
        ('O', 2, [['O', 'O'], ['O', 'O']]),
        ('Z', 1, [['.', 'Z'], ['Z', 'Z'], ['Z', '.']]),
    ],
)
def test_rotate(tile, rotation, expected):
    assert rotate(TETROMINO_SHAPES[tile], rotation) == expected


@pytest.mark.parametrize(
    "tile,board_x,board_y,fits",
    [
        ('I', 4, 1, True),
        ('I', 2, 1, False),
    ],
)
def test_tile_fits_clean_board_pos_0(tile, board_x, board_y, fits):
    s = TetrominoSolver([tile], board_x, board_y)
    assert s.tile_fits(tile, 0, 0, 0) == fits


@pytest.mark.parametrize(
    "tiles,board_x,board_y,solution",
    [
        (['O', 'O', 'O', 'O'], 4, 4, [(0, 'O', 0), (2, 'O', 0), (8, 'O', 0), (10, 'O', 0)]),
    ],
)
def test_solve(tiles, board_x, board_y, solution):
    s = TetrominoSolver(tiles, board_x, board_y)
    s.solve()
    assert list(s.solution) == solution
