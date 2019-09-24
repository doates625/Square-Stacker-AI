'''
GameState.py
Square Stacker game emulator class
'''

from random import randint

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
        self.colors = list('PGBYOV')
        self.num_colors = len(self.colors)

        # Initialize Empty Board
        self.board = []
        self.piece = []
        for i in range(3):
            self.board.append([])
            for j in range(3):
                self.board[i].append([])
                for n in range(3):
                    self.board[i][j].append('_')
            self.piece.append([])
            for n in range(3):
                self.piece[i].append('_')

        # Scoring coutners
        self.score = 0
        self.combo = 0

        # Add random tile piece
        self._add_pieces()

    def get_valid_moves(self):
        '''
        List of valid moves for given state

        Moves have the form [k, i, j]
        Moving piece k to board tile [i, j]
        '''
        moves = []
        for k in self._playable_piece():
            for i in range(3):
                for j in range(3):
                    move = [k, i, j]
                    if self._is_move_valid(move):
                        moves.append(move)
        return moves

    def make_move(self, move):
        '''
        Applies move to game board (if valid)
        Returns points for this move
        '''

        if self._is_move_valid(move):

            # Parse move
            k, i, j = self._parse_move(move)

            # Transfer tiles
            for n in range(3):
                c = self.piece[k][n]
                if c != '_':
                    self.board[i][j][n] = c
                    self.piece[k][n] = '_'

            # Delete cleared tials
            points = 0
            # TODO delete cleared tiles
            # TODO calculate points for move

            # Update score and combo
            self.score += points
            if points > 0:
                self.combo += 1
                points *= self.combo
                self.score += points
            else:
                self.combo = 0

            # Make more piece if all empty
            piece_empty = True
            for k in range(3):
                if self._is_piece_playable(k):
                    piece_empty = False
                    break
            if piece_empty:
                self._add_pieces()

            # Return points
            return points

    def get_score(self):
        '''
        Returns total score of game so far
        '''
        return self.score

    def _add_pieces(self):
        '''
        Adds three random pieces to the game
        '''

        # For each piece tile
        for k in range(3):
            c = randint(0, self.num_colors - 1)
            n = randint(0, 2)
            self.piece[k][n] = self.colors[c]

    def _is_move_valid(self, move):
        '''
        Returns if given move is valid
        '''

        # Parse move
        k, i, j = self._parse_move(move)

        # Verify piece is playable
        if not self._is_piece_playable(k):
            return False

        # Check for color overlaps
        for n in range(3):
            if self.board[i][j][n] != '_' and self.piece[k][n] != '_':
                return False
        return True

    def _playable_piece(self):
        '''
        Returns list of playable piece k [0:2]
        '''
        piece = []
        for k in range(3):
            if self._is_piece_playable(k):
                piece.append(k)
        return piece

    def _is_piece_playable(self, k):
        '''
        Returns true if piece i [0:2] is non-empty
        '''
        for n in range(3):
            if self.piece[k][n] != '_':
                return True
        return False

    def _parse_move(self, move):
        '''
        Returns k,i,j of move
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
                    msg += self.board[i][j][k]
                    if k < 2:
                        msg += ' '
                msg += '] '

            # Print piece tile [i]
            msg += '| ['
            for k in range(3):

                # Print inner, middle, outer
                msg += self.piece[i][k]
                if k < 2:
                    msg += ' '
            msg += ']'

            # Print newline
            if i < 2:
                msg += '\n'
            
        return msg
    
