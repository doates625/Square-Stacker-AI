"""
SquareStackerGame.py
Square Stacker game emulator class

Game State Encoding:
Board
    _board[i][j] = tile at row i [0..2] column j [0..2]
    _piece[k] = tile at row k [0..2]
Tiles
    tile[0] = Inner color
    tile[1] = Middle color
    tile[2] = Outer color
Colors
    '_' = Empty
    'P' = Pink
    'G' = Green
    'B' = Blue
    'Y' = Yellow
    'O' = Orange
    'V' = Violet
Moves
    move = [k, i, j]
    Moves _piece[k] to _board [i][j]
Scoring
    _score = Points scored so far
    _combo = Number of scores in a row
"""

import numpy as np
from random import randint
from copy import deepcopy
from operator import add
from typing import List


def move_to_index(move):
    """
    Converts move to 1D index
    :param move: Game move [k,i,j]
    :return: Index [0..26]
    """
    k, i, j = move
    return (9 * k) + (3 * i) + j


def index_to_move(n):
    """
    Converts 1D index to move
    :param n: Index of move [0..26]
    :return: Game move [k,i,j]
    """
    k = n // 9
    n = n % 9
    i = n // 3
    j = n % 3
    return [k, i, j]


def move_to_vector(move):
    """
    Converts move to normalized 27D vector
    :param move: Game move [k,i,j]
    :return: List of 27 zeros with 1 on index of move
    """
    vector = [0] * 27
    vector[move_to_index(move)] = 1
    return vector


def vector_to_move(vector):
    """
    Converts 27D move vector to move
    :param vector: List of 27 zeros with 1 on index of move
    :return: Game move [k,i,j]
    """
    index = np.argmax(vector)
    move = index_to_move(index)
    return move


class SquareStackerGame:

    _colors: List[str] = ['P', 'G', 'B', 'Y', 'O', 'V']  # Piece colors
    _num_colors: int = len(_colors)  # Number of piece colors

    def __init__(self):
        """
        Initializes new Square Stacker game.
        """

        # Initialize Empty Board
        self._board = []
        self._piece = []
        for i in range(3):
            self._board.append([])
            for j in range(3):
                self._board[i].append([])
                for n in range(3):
                    self._board[i][j].append('_')
            self._piece.append([])
            for n in range(3):
                self._piece[i].append('_')

        # Game state variables
        self._is_piece_playable = [False, False, False]

        # Scoring counters
        self._score = 0
        self._combo = 0

        # Add random tile piece
        self._add_pieces()

    def get_valid_moves(self):
        """
        :return: List of valid moves for current game state
        """
        moves = []
        for k in range(3):
            if self._is_piece_playable[k]:
                for i in range(3):
                    for j in range(3):
                        move = [k, i, j]
                        if self.is_move_valid(move):
                            moves.append(move)
        return moves

    def is_move_valid(self, move):
        """
        Checks validity of game move
        :param move: Move to check
        :return Boolean indicating validity
        """

        # Parse move
        k, i, j = move

        # Verify piece is playable
        if not self._is_piece_playable[k]:
            return False

        # Check for color overlaps
        for n in range(3):
            if self._board[i][j][n] != '_' and self._piece[k][n] != '_':
                return False
        return True

    def make_move(self, move):
        """
        Applies move to game board (if valid)
        :param move: Move to make
        :return: Points for this move
        """

        # Check if move is valid
        points = 0
        if self.is_move_valid(move):

            # Parse move
            k, i, j = move

            # Only check colors on piece
            piece_colors = set(self._piece[k])
            piece_colors.remove('_')

            # Transfer piece to board
            for n in range(3):
                c = self._piece[k][n]
                if c != '_':
                    self._board[i][j][n] = c
                    self._piece[k][n] = '_'
            self._is_piece_playable[k] = False

            # Make new game board and calculate clear points
            new_board = deepcopy(self._board)

            # Process rows and columns
            row_clears = self._process_line(lambda m: i, lambda m: m, piece_colors, new_board)
            col_clears = self._process_line(lambda m: m, lambda m: j, piece_colors, new_board)
            color_clears = list(map(add, row_clears, col_clears))

            # Process diagonals
            if i == j:
                pos_clears = self._process_line(lambda m: m, lambda m: 0 + m, piece_colors, new_board)
                color_clears = list(map(add, color_clears, pos_clears))
            if i == 2 - j:
                neg_clears = self._process_line(lambda m: m, lambda m: 2 - m, piece_colors, new_board)
                color_clears = list(map(add, color_clears, neg_clears))

            # Add up total points
            points = 3 * sum(map(lambda x: x**2, color_clears))
            points += self._process_tile(i, j, new_board)

            # Update score and combo
            if points > 0:
                self._combo += 1
                points *= self._combo
                self._score += points
            else:
                self._combo = 0

            # Update game board
            self._board = new_board
            self._add_pieces()

        # Return points
        return points

    def _process_line(self, i_func, j_func, check_colors, new_board):
        """
        Processes color clears in line parameterized by [i_func, j_func]
        :param i_func: Returns i for m in range(2)
        :param j_func: Returns j for m in range(2)
        :param check_colors: Set of colors to check
        :param new_board: Board to have colors removed from
        :return: Array of number of clears for each color [0 or 1]
        """

        # Pre-calculate i and j vectors
        i = list(map(i_func, range(3)))
        j = list(map(j_func, range(3)))

        # Find cleared colors
        cleared_colors = deepcopy(check_colors)
        cleared_array = [1] * self._num_colors
        for m in range(3):
            for c in range(self._num_colors):
                color = self._colors[c]
                if color not in self._board[i[m]][j[m]]:
                    cleared_array[c] = 0
                    if color in cleared_colors:
                        cleared_colors.remove(color)

        # Remove colors from board
        for m in range(3):
            for n in range(3):
                if self._board[i[m]][j[m]][n] in cleared_colors:
                    new_board[i[m]][j[m]][n] = '_'

        # Returns
        return cleared_array

    def _process_tile(self, i, j, new_board):
        """
        Returns points cleared in given tile
        :param i: Index of played row [0-2]
        :param j: Index of played column[0-2]
        :param new_board: Board to have colors removed from
        :return: Points for tile clear
        """
        tile = self._board[i][j]
        if tile[0] == tile[1] == tile[2]:
            new_board[i][j] = ['_', '_', '_']
            return 5
        else:
            return 0

    def _add_pieces(self):
        """
        Adds three random pieces to the game if none are playable
        """

        # Check if no pieces are left
        if True not in self._is_piece_playable:

            # For each game piece
            for k in range(3):
                # Add random color to piece
                c = randint(0, self._num_colors - 1)
                n = randint(0, 2)
                self._piece[k][n] = self._colors[c]

                # Mark piece as playable
                self._is_piece_playable[k] = True

    def get_board(self):
        """
        :return: Copy of game board
        """
        return deepcopy(self._board)

    def get_piece(self):
        """
        :return: Copy of game pieces
        """
        return deepcopy(self._piece)

    def get_score(self):
        """
        :return: Current game score
        """
        return self._score

    def get_combo(self):
        """
        :return: Current game combo count
        """
        return self._combo

    def get_state_vector(self, encoding='state'):
        """
        Converts game state to a numeric vector
        :param encoding: 'color' or 'state'
        :return: State vector representing game [np.array]
        """
        vector = []
        colors = ['_'] + self._colors
        if encoding == 'color':

            # Numerical color encoding
            for i in range(3):
                for j in range(3):
                    for n in range(3):
                        color = self._board[i][j][n]
                        vector.append(colors.index(color))
            for k in range(3):
                for n in range(3):
                    color = self._piece[k][n]
                    vector.append(colors.index(color))
            vector.append(self._score)
            vector.append(self._combo)

        elif encoding == 'state':

            # State-vector color encoding
            for i in range(3):
                for j in range(3):
                    for n in range(3):
                        color = self._board[i][j][n]
                        color_vector = [0.0] * len(colors)
                        color_vector[colors.index(color)] = 1.0
                        vector += color_vector
            for k in range(3):
                for n in range(3):
                    color = self._piece[k][n]
                    color_vector = [0.0] * len(colors)
                    color_vector[colors.index(color)] = 1.0
                    vector += color_vector
            vector.append(self._score)
            vector.append(self._combo)

        # Return vector
        return np.array(vector)

    def __str__(self):
        """
        String converter
        """
        msg = ''

        # Print each row [i]
        for i in range(3):

            # Print each board tile [j]
            for j in range(3):
                msg += '['

                # Print inner, middle, outer
                for k in range(3):
                    msg += self._board[i][j][k]
                    if k < 2:
                        msg += ' '
                msg += '] '

            # Print piece tile [i]
            msg += '| ['
            for k in range(3):

                # Print inner, middle, outer
                msg += self._piece[i][k]
                if k < 2:
                    msg += ' '
            msg += ']\n'

        # Print score and combo
        msg += 'Score: ' + str(self._score) + '\t'
        msg += 'Combo: ' + str(self._combo)

        return msg
