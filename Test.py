"""
Test.py
Square Stacker game test script
"""

from SquareStackerGame import *
from random import randint

# Create new game
game = SquareStackerGame()

# Play randomly until board fills
num_moves = 1
while True:

    # Get valid moves
    valid_moves = game.get_valid_moves()
    num_valid_moves = len(valid_moves)

    # Check if any moves exist
    if num_valid_moves > 0:

        # Make random move
        m = randint(0, num_valid_moves - 1)
        move = valid_moves[m]
        k, i, j = move
        game.make_move(move)

        # Display results
        print('Move ' + str(num_moves) + ':')
        print('Piece [' + str(k+1) + '] to Board [' + str(i+1) + ',' + str(j+1) + ']:')
        print(str(game) + '\n')

        # Increment move counter
        num_moves += 1
        
    else:

        # Exit game
        print('No moves left!')
        break
