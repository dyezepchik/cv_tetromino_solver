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
        ('T', 1, [['.', 'T'], ['T', 'T'], ['.', 'T']]),
        ('T', 2, [['.', 'T', '.'], ['T', 'T', 'T']]),
        ('T', 3, [['T', '.'], ['T', 'T'], ['T', '.']]),
        ('L', 1, [['L', 'L'], ['.', 'L'], ['.', 'L']]),
        ('L', 2, [['.', '.', 'L'], ['L', 'L', 'L']]),
        ('L', 3, [['L', '.'], ['L', '.'], ['L', 'L']]),
    ],
)
def test_rotate(tile, rotation, expected):
    assert rotate(TETROMINO_SHAPES[tile], rotation) == expected


@pytest.mark.parametrize(
    "tile,rotation,pos_x,pos_y,expected",
    [
        ('L', 0, 1, 0, ['.', 'L', 'L', 'L',
                        '.', 'L', '.', '.',
                        '.', '.', '.', '.',
                        '.', '.', '.', '.']),
        ('L', 1, 1, 0, ['.', 'L', 'L', '.',
                        '.', '.', 'L', '.',
                        '.', '.', 'L', '.',
                        '.', '.', '.', '.']),
    ],
)
def test_add_tile_empty_board(tile, rotation, pos_x, pos_y, expected):
    s = TetrominoSolver([tile], 4, 4)
    s.add_tile(tile, rotation, pos_x, pos_y)
    assert s.board == expected


@pytest.mark.parametrize(
    "tiles,expected",
    [
        ((('S', 1, 0, 0), ('L', 1, 1, 0)), ['S', 'L', 'L', '.',
                                            'S', 'S', 'L', '.',
                                            '.', 'S', 'L', '.']),
    ],
)
def test_add_tile_non_empty_board(tiles, expected):
    tls = [x[0] for x in tiles]
    s = TetrominoSolver(tls, 4, 3)
    for tile_params in tiles:
        tile, rotation, pos_x, pos_y = tile_params
        s.add_tile(tile, rotation, pos_x, pos_y)
    assert s.board == expected


@pytest.mark.parametrize(
    "tile,rotation,pos_x,pos_y",
    [
        ('L', 0, 1, 0),
        ('L', 1, 1, 0),
        ('Z', 1, 0, 1),
        ('S', 2, 1, 0),
        ('T', 3, 1, 1),
    ],
)
def test_remove_tile_empty_board(tile, rotation, pos_x, pos_y):
    s = TetrominoSolver([tile], 4, 4)
    s.add_tile(tile, rotation, pos_x, pos_y)
    s.rem_tile(tile, rotation, pos_x, pos_y)
    assert s.board == ['.'] * 16


@pytest.mark.parametrize(
    "tile,rotation,board_x,board_y,fits",
    [
        ('I', 0, 4, 1, True),
        ('I', 1, 1, 4, False),
        ('I', 2, 4, 1, True),
        ('I', 3, 1, 4, False),
        ('I', 0, 2, 1, False),
        ('I', 1, 1, 2, False),
        ('I', 2, 2, 1, False),
        ('I', 3, 1, 2, False),
    ],
)
def test_tile_fits_clean_board_pos_0(tile, rotation, board_x, board_y, fits):
    s = TetrominoSolver([tile], board_x, board_y)
    assert s.tile_fits(tile, 0, 0, 0) == fits


@pytest.mark.parametrize(
    "tiles,board_x,board_y,solution",
    [
        (['O', 'O', 'O', 'O'], 4, 4, [(0, 'O', 0), (2, 'O', 0), (8, 'O', 0), (10, 'O', 0)]),
        (['L', 'L', 'S'], 4, 3, "exists"),
        (['S', 'L', 'L'], 4, 3, "exists"),
        (['L', 'S', 'L'], 4, 3, "exists"),
        (['T', 'L', 'S', 'T', 'I'], 5, 4, "exists"),
        (['L', 'T', 'T', 'S', 'I'], 5, 4, "exists"),
        (['I', 'T', 'L', 'S', 'T'], 5, 4, "exists"),
    ],
)
def test_solve(tiles, board_x, board_y, solution):
    s = TetrominoSolver(tiles, board_x, board_y)
    res = s.solve()
    if solution == "exists":
        assert res != -1
    elif solution is None:
        assert res == -1
    else:
        assert list(s.solution) == solution
