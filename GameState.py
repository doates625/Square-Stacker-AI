'''
GameState.py
Square Stacker game emulator class
'''

class GameState:

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

        Game Pieces
        piece[i] = tile at row i
        i = 0:2

        Combo Counter
        combos = Number of scores in a row
        '''

        # Initialize Empty Board
        self.board = [[['_']*3]*3]*3
        self.pieces = [['_']*3]*3
        self.combos = 0

        # Add random tile pieces
        self.add_pieces()

    def add_pieces(self):
        '''
        Adds random pieces to the board
        '''
        # TODO

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
                msg += self.pieces[i][k]
                if k < 2:
                    msg += ' '
            msg += ']'

            # Print newline
            if i < 2:
                msg += '\n'
            
        return msg
    
