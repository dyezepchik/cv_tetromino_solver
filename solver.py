#!/usr/bin/env python3

""" Notes for algo:
 - no need to rotate O
 - I - only two possible rotations
 - add non-recursive solution
 - add optimized solution
 - 
"""

import argparse
import typing
from collections import deque

# Define the shapes of the single parts (no need for mirrored ones) 4x4
# tetromino_shapes = {
#     "I": "..X...X...X...X.",
#     "Z": "..X..XX...X.....",  # mirrored
#     "O": ".....XX..XX.....",
#     "L": ".X...X...XX.....",  # mirrored
#     "T": "..X..XX...X.....",
# }
# Alternative shapes definitions
TETROMINO_SHAPES = {
    'I': (('I', 'I', 'I', 'I'), ),
    'Z': (('Z', 'Z', '.'),
          ('.', 'Z', 'Z')),
    'S': (('.', 'S', 'S'),
          ('S', 'S', '.')),
    'O': (('O', 'O'),
          ('O', 'O')),
    'L': (('L', 'L', 'L'),
          ('L', '.', '.')),
    'J': (('J', '.', '.'),
          ('J', 'J', 'J')),
    'T': (('T', 'T', 'T'),
          ('.', 'T', '.')),
}
"""
pipenv run ./solver.py T L S T I  --board-x 5 --board-y 4
T I I I I
T T T T T
T S S T L
S S L L L
deque([(0, 'L', 3), (1, 'S', 1), (8, 'T', 1), (2, 'T', 0), (15, 'I', 0)])
"""
def rotate_clockwise(matrix: [[str]]):
    return [list(reversed(col)) for col in zip(*matrix)]

def rotate(tile_def: [[str]], rotation):
    if rotation == 0:
        return tile_def
    tile_def = rotate_clockwise(tile_def)
    if rotation == 1:
        return tile_def
    tile_def = rotate_clockwise(tile_def)
    if rotation == 2:
        return tile_def
    tile_def = rotate_clockwise(tile_def)
    if rotation == 3:
        return tile_def

    raise ValueError("Wrong rotation value")

class TetrominoSolver:

    def __init__(self, tiles: [str], board_x: int, board_y: int):
        # given
        self.tiles = tiles
        self.board_x = board_x
        self.board_y = board_y
        # for solution
        self.board = ['.'] * board_x * board_y
        self.solution = deque()  # used as stack
        self.remaining_tiles = deque()  # used as circular buffer

    def draw_board(self):
        res = ""
        offset = 0
        while line:=self.board[offset:offset+self.board_x]:
            res += "".join(line) + "\n"
            offset += self.board_x
        return "\n" + res

    def tile_fits(self, tile: str, rotation: int, position_x: int, position_y: int):
        tile_rotated = rotate(TETROMINO_SHAPES[tile], rotation)
        for y, line in enumerate(tile_rotated):
            for x, val in enumerate(line):
                if position_x + x < 0 or position_x + x >= self.board_x:
                    return False

                if position_y + y < 0 or position_y + y >= self.board_y:
                    return False

                board_idx = (position_y + y) * self.board_x + (position_x + x)

                if val != '.' and self.board[board_idx] != '.':
                    return False

        return True

    def add_tile(self, tile, rotation, position_x: int, position_y: int):
        tile_rotated = rotate(TETROMINO_SHAPES[tile], rotation)
        for y, line in enumerate(tile_rotated):
            for x, val in enumerate(line):
                board_idx = (position_y + y) * self.board_x + (position_x + x)
                if val == tile:
                    self.board[board_idx] = val

    def rem_tile(self, tile, rotation, position_x: int, position_y: int):
        tile_rotated = rotate(TETROMINO_SHAPES[tile], rotation)
        for y, line in enumerate(tile_rotated):
            for x, val in enumerate(line):
                board_idx = (position_y + y) * self.board_x + (position_x + x)
                if val == tile:
                    self.board[board_idx] = '.'

    def _solve(self, board, tiles):
        # print(self.draw_board())
        # find first empty cell on the board at the moment
        index = None
        for i, cell in enumerate(board):
            if cell == '.':
                index = i
            else:
                continue

            cell_y, cell_x = index // self.board_x, index % self.board_x
            for i, tile in enumerate(tiles):
                for rotation in range(4):
                    if self.tile_fits(tile, rotation, cell_x, cell_y):
                        # add to the board, add to solution, call recursively
                        self.add_tile(tile, rotation, cell_x, cell_y)
                        self.solution.append((index, tile, rotation))
                        res = self._solve(board, tiles[:i]+tiles[i+1:])
                        if res == -1:
                            self.rem_tile(tile, rotation, cell_x, cell_y)
                            self.solution.pop()
                            continue

                        return

        if index is None:
            return  # Problem solved
            # raise RuntimeError("Something went wrong. No empty cells on the board.")

        # # if no solution found for board cell 'index', try vacant neighbour cells
        # for cell in 
        return -1  # remove previous tile

    def solve(self):
        res = self._solve(self.board, self.tiles)
        if res == -1:
            raise RuntimeError("No solution found.")


if __name__ == "__main__":
    "Sample run: ./solver.py O O O O --board-x 4 --board-y 4"
    parser = argparse.ArgumentParser(description='For testing from command line.')
    parser.add_argument('tiles', metavar='N', type=str, nargs='+', help='array of tiles')
    parser.add_argument('--board-x', help='Board size X')
    parser.add_argument('--board-y', help='Board size Y')

    args = parser.parse_args()

    tetromino = TetrominoSolver(args.tiles, int(args.board_x), int(args.board_y))
    tetromino.solve()
    print(tetromino.solution)

