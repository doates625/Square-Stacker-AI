"""
agent.py
Superclass for Square Stacker AI memory agents
"""

from typing import List
from agents.agent import Agent
import random as rand


# Colors
#     '_' = Empty
#     'P' = Pink
#     'G' = Green
#     'B' = Blue
#     'Y' = Yellow
#     'O' = Orange
#     'V' = Violet


class MemoryAgent(Agent):

    def __init__(self, memory_length=5):
        """
        Empty constructor
        """
        Agent.__init__(self)
        self.memoryLength = 1
        self.color_memory = ['']*memory_length  # previous color
        self.move_memory = [[]]*memory_length  # previous move location [piece, i, j]
        self.piece_memory = [[]]*memory_length  # previously played piece structure
        self._colors: List[str] = ['_', 'P', 'G', 'B', 'Y', 'O', 'V']  # Piece colors
        self._to_update = 0
        self._update_limit = memory_length-1

    def select_move(self, game):
        """
        Selects next move to make for given game
        :param game: Current game [SquareStackerGame]
        :return move: Move [k, i, j] or None if no moves exist
        """

        g = game.get_state_vector(encoding="color")  # board [3x3x3] + available moves [1x3x3] + score + combo

        board_as_char = []
        for i in range(len(g) - 3):  # exclude score and combo from board_as_char
            board_as_char.append(self._colors[g[i]])

        pieces = game.get_piece()
        match_flag = False
        piece_match_index = 0
        color_match_index = 0

        # identify available pieces that match the color in the agent memory
        for i in pieces:
            for j in self.color_memory:
                if j in i:
                    match_flag = True
                    piece_match_index = pieces.index(i)
                    color_match_index = self.color_memory.index(j)

        # if memory is empty or the offered pieces do not contain the color previously placed
        if self.color_memory[0] == '' or not match_flag:
            valid_moves = game.get_valid_moves()
            num_valid_moves = len(valid_moves)

            # as long as the agent can make a move
            if num_valid_moves > 0:
                # randomize a move in the set of valid moves
                m = rand.randint(0, num_valid_moves - 1)

                # save the color, piece structure, and play location to memory
                piece_to_place = game.get_piece()[valid_moves[m][0]]
                color_to_place = []
                for i in range(len(piece_to_place)):
                    if piece_to_place[i] != '_':
                        color_to_place = (piece_to_place[i])  # extract the color of the piece being played
                self.color_memory[self._to_update] = color_to_place  # save the color
                self.piece_memory[self._to_update] = piece_to_place
                self.move_memory[self._to_update] = valid_moves[m]  # and the play location to agent memory
                if self._to_update < self._update_limit:
                    self._to_update += 1
                else:
                    self._to_update = 0

                # return the move [k, i, j] to be played
                return valid_moves[m]
            else:
                return None
        else:
            previous_move = self.move_memory[color_match_index]
            # get the [i, j] of old move that color matched one of the available pieces
            previous_i = previous_move[1]
            previous_j = previous_move[2]

            check = [-1, 0, 1]

            # check adjacent tiles for space availability to place matching piece
            for i in range(3):
                for j in range(3):

                    check_i = previous_i + check[i]
                    check_j = previous_j + check[j]

                    # limit to manhattan adjacents
                    if not (check_i == check_j or check_i+check_j == 0):


                        # only check for valid moves if the indices are within the board
                        if 0 <= check_i <= 2 and 0 <= check_j <= 2:

                            valid_moves = game.get_valid_moves()
                            piece_moves = []
                            # get all of the valid moves for the piece that matched the color of the previous move
                            for move in valid_moves:
                                if move[0] == piece_match_index:
                                    piece_moves.append(move)



                            # use the first listed move that matches the adjacent tile
                            for moves in piece_moves:
                                if moves[1] == check_i and moves[2] == check_j:
                                    color_to_place = []
                                    for k in range(len(pieces[piece_match_index]) - 1):
                                        # Extract the color of the piece being played
                                        if pieces[piece_match_index][k] != '_':
                                            color_to_place = (pieces[piece_match_index][k])

                                    self.color_memory[self._to_update] = color_to_place  # save the color
                                    self.piece_memory[self._to_update] = pieces[piece_match_index]
                                    self.move_memory[self._to_update] = moves  # and the play location to agent memory

                                    if self._to_update < self._update_limit:
                                        self._to_update += 1
                                    else:
                                        self._to_update = 0

                                    return moves
            # if it cannot find an adjacent space near its match then do a random move
            valid_moves = game.get_valid_moves()
            num_valid_moves = len(valid_moves)
            if num_valid_moves > 0:

                # randomize a move in the set of valid moves
                m = rand.randint(0, num_valid_moves - 1)

                # save the color, piece structure, and play location to memory
                piece_to_place = game.get_piece()[valid_moves[m][0]]
                color_to_place = []
                for i in range(len(piece_to_place) - 1):
                    if piece_to_place[i] != '_':
                        color_to_place = (piece_to_place[i])  # extract the color of the piece being played

                self.color_memory[self._to_update] = color_to_place  # save the color
                self.piece_memory[self._to_update] = piece_to_place
                self.move_memory[self._to_update] = valid_moves[m]  # and the play location to agent memory

                if self._to_update < self._update_limit:
                    self._to_update += 1
                else:
                    self._to_update = 0

                return valid_moves[m]
            else:
                return None

