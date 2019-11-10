"""
agent.py
Superclass for Square Stacker AI search agents
"""

from agents.agent import Agent


class SearchAgent(Agent):

    def __init__(self):
        """
        Empty constructor
        """
        Agent.__init__(self)

    def select_move(self, game):
        """
        Selects next move to make for given game
        :param game: Current game [SquareStackerGame]
        :return move: Move [k, i, j] or None if no moves exist
        :return moves_searched: Number of moves searched before deciding
        """
        return None, 0
