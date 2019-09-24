'''
Test.py
Square Stacker game test script
'''

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

        # Show Game board
        print('Move ' + str(num_moves) + ':')
        print(game)

        # Generate random move
        m = randint(0, num_valid_moves - 1)
        move = valid_moves[m]
        k = move[0]
        i = move[1]
        j = move[2]

        # Apply move
        print('Piece [' + str(k) + '] to Board [' + str(i) + ',' + str(j) + ']:')
        points = game.make_move(move)
        score = game.get_score()
        combo = game.get_combo()
        print(game)
        print('Points earned: ' + str(points))
        print('Total score: ' + str(score))
        print('Combo count: ' + str(combo) + '\n')

        # Increment move counter
        num_moves += 1
        
    else:

        # Exit game
        print('No moves left!')
        break
