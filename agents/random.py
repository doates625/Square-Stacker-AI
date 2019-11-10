"""
random_.py
Square Stacker AI agent which makes random moves (baseline)
"""

from agents.agent import Agent
from numpy.random import randint


class RandomAgent(Agent):

    def __init__(self):
        """
        Empty constructor
        """
        Agent.__init__(self)

    def select_move(self, game):
        """
        Uniformly randomly selects moves from valid moves
        :param game: Current game [SquareStackerGame]
        :return: Move [k, i, j] or None if no moves exist
        """
        valid_moves = game.get_valid_moves()
        num_valid_moves = len(valid_moves)
        if num_valid_moves > 0:
            m = randint(0, num_valid_moves)
            return valid_moves[m]
        else:
            return None
