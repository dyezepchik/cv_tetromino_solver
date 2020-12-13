#!/usr/bin/env python3

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
tetromino_shapes = {
    'I': [['I', 'I', 'I', 'I']],
    'Z': [['Z', 'Z', '.']
          ['.', 'Z', 'Z']],
    'S': [['.', 'S', 'S']
          ['S', 'S', '.']],
    'O': [['O', 'O'],
          ['O', 'O']],
    'L': [['L', 'L', 'L'],
          ['L', '.', '.']],
    'J': [['J', '.', '.'],
          ['J', 'J', 'J']],
    'T': [['T', 'T', 'T'],
          ['.', 'T', '.']],
}

def rotate_clockwise(matrx: [[str]]):
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
        self.board = ["."] * board_x * board_y
        self.solution = deque()  # used as stack
        self.remaining_tiles = deque()  # used as circular buffer

    def draw_solution(self):
        res = ""
        offset = 0
        while line:=self.board[offset:offset+self.board_x]:
            res += "".join(line) + "\n"
            offset += self.board_x
        return res

    def tile_fits(self, tile: str, rotation: int, position_x: int, position_y: int):
        pass

    def solve(self):
        """
        1. find the first vacant cell on the board (starting from upper left corner)
        2. Try to fit unfitted tiles onto the board starting from that cell
        3. If none fit - step back
        """
        solution_found = False
        while not solution_found:
            for tile in self.tiles:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='For testing from command line.')
    parser.add_argument('tiles', metavar='N', type=str, nargs='+', help='array of tiles')
    parser.add_argument('--board-x', help='Board size X')
    parser.add_argument('--board-y', help='Board size Y')

    args = parser.parse_args()

    tetromino = TetrominoSolver(args.tiles, int(args.board_x), int(args.board_y))

    print(tetromino.solution)
