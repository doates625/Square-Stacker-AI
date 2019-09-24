'''
GameState.py
Square Stacker game emulator class
'''

from random import randint
from copy import deepcopy

class SquareStackerGame:

    def __init__(self):
        '''
        Class constructor

        Game Colors
        '_' = Empty
        'P' = Pink
        'G' = Green
        'B' = Blue
        'Y' = Yellow
        'O' = Orange
        'V' = Violet

        Game Tiles
        tile[0] = Inner color
        tile[1] = Middle color
        tile[2] = Outer color

        Game Board
        board[i][j] = tile at row i column j
        i = 0:2
        j = 0:2

        Game piece
        piece[k] = tile at row k
        k = 0:2

        Scoring
        score = Points scored so far
        combo = Number of scores in a row
        '''

        # Constants
        self._colors = list('PGBYOV')
        self._num_colors = len(self._colors)

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
        '''
        List of all valid moves for given state

        Moves have the form [k, i, j]
        Moving piece k to board tile [i, j]
        '''
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
        '''
        Returns if given move is valid
        '''

        # Parse move
        k, i, j = self._parse_move(move)

        # Verify piece is playable
        if not self._is_piece_playable[k]:
            return False

        # Check for color overlaps
        for n in range(3):
            if self._board[i][j][n] != '_' and self._piece[k][n] != '_':
                return False
        return True

    def make_move(self, move):
        '''
        Applies move to game board (if valid)
        Returns points for this move
        '''

        # Check if move is valid
        points = 0
        if self.is_move_valid(move):

            # Parse move
            k, i, j = self._parse_move(move)

            # Transfer piece to board
            for n in range(3):
                c = self._piece[k][n]
                if c != '_':
                    self._board[i][j][n] = c
                    self._piece[k][n] = '_'
            self._is_piece_playable[k] = False

            # Delete cleared tials
            new_board = deepcopy(self._board)
            
            # Look for cleared rows
            for i in range(3):

                # Detect cleared row colors
                row_colors = deepcopy(self._colors)
                for j in range(3):
                    for c in self._colors:
                        if c in row_colors and c not in self._board[i][j]:
                            row_colors.remove(c)

                # Add points for each color
                points += 3*len(row_colors)

                # Remove colors from board
                for j in range(3):
                    for n in range(3):
                        if self._board[i][j][n] in row_colors:
                            new_board[i][j][n] = '_'

            # Look for cleared columns
            for j in range(3):

                # Detect cleared column colors
                col_colors = deepcopy(self._colors)
                for i in range(3):
                    for c in self._colors:
                        if c in col_colors and c not in self._board[i][j]:
                            col_colors.remove(c)

                # Add points for each color
                points += 3*len(col_colors)

                # Remove colors from board
                for i in range(3):
                    for n in range(3):
                        if self._board[i][j][n] in col_colors:
                            new_board[i][j][n] = '_'

            # Detect cleared diagonal colors
            pos_colors = deepcopy(self._colors)
            neg_colors = deepcopy(self._colors)
            for i in range(3):
                for c in self._colors:
                    if c in pos_colors and c not in self._board[i][i]:
                        pos_colors.remove(c)
                for c in self._colors:
                    if c in neg_colors and c not in self._board[i][2-i]:
                        neg_colors.remove(c)

            # Add points for each color
            points += 3*len(pos_colors)
            points += 3*len(neg_colors)

            # Remove diagonal colors from board
            for i in range(3):
                for n in range(3):
                    if self._board[i][i][n] in pos_colors:
                        new_board[i][i][n] = '_'
                    if self._board[i][2-i][n] in neg_colors:
                        new_board[i][2-i][n] = '_'

            # Look for cleared singles
            for i in range(3):
                for j in range(3):

                    # Check if board[i][j] has all same color
                    c0 = self._board[i][j][0]
                    c1 = self._board[i][j][1]
                    c2 = self._board[i][j][2]
                    if c0 != '_' and c0 == c1 and c0 == c2:

                        # Add points
                        points += 5

                        # Remove single tile from board
                        for n in range(3):
                            new_board[i][j][n] = '_'

            # Update game board
            self._board = new_board

            # Update score and combo
            if points > 0:
                self._combo += 1
                points *= self._combo
                self._score += points
            else:
                self._combo = 0

            # Add more pieces if all empty
            self._add_pieces()

        # Return points
        return points

    def get_score(self):
        '''
        Returns current game score
        '''
        return self._score

    def get_combo(self):
        '''
        Returns current game combo count
        '''
        return self._combo

    def _add_pieces(self):
        '''
        Adds three random pieces to the game if none are playable
        '''

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

    def _playable_pieces(self):
        '''
        Returns list of playable piece k [0:2]
        '''
        piece = []
        for k in range(3):
            
                piece.append(k)
        return piece

    def _parse_move(self, move):
        '''
        Returns k, i, j of move
        '''
        k = move[0]
        i = move[1]
        j = move[2]
        return k, i, j

    def __str__(self):
        '''
        String converter
        '''
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
            msg += ']'

            # Print newline
            if i < 2:
                msg += '\n'
            
        return msg
