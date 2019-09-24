"""
Test.py
Square Stacker game test script
"""

from SquareStackerGame import SquareStackerGame
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

        # Generate random move
        m = randint(0, num_valid_moves - 1)
        move = valid_moves[m]
        k = move[0] + 1
        i = move[1] + 1
        j = move[2] + 1

        # Apply move
        print('Move ' + str(num_moves) + ':')
        print('Piece [' + str(k) + '] to Board [' + str(i) + ',' + str(j) + ']:')
        game.make_move(move)
        print(str(game) + '\n')

        # Increment move counter
        num_moves += 1
        
    else:

        # Exit game
        print('No moves left!')
        break
