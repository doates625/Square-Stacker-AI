"""
agent.py
Superclass for Square Stacker AI agents
"""


class Agent:

    def __init__(self):
        """
        Empty constructor
        """
        pass

    def select_move(self, game):
        """
        Selects next move to make for given game
        :param game: Current game [SquareStackerGame]
        :return: Move [k, i, j] or None if no moves exist
        """
        return None
