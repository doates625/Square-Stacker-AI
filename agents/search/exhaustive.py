"""
exhaustive.py
Class for Square Stacker Exhaustive search Agent

The exhaustive search agent searches all possible move sequences of a finite length
and selects the move which maximizes score.
"""

import numpy as np
from agents.search.agent import SearchAgent


class ExhaustiveSearchAgent(SearchAgent):

    def __init__(self, search_depth):
        """
        Constructs exhaustive search agent
        :param search_depth: Number of moves ahead to search
        """
        SearchAgent.__init__(self)
        self._search_depth = search_depth

    def select_move(self, game):
        """
        Selects next move to make for given game
        :param game: Current game [SquareStackerGame]
        :return: Move [k, i, j] or None if no moves exist
        :return moves_searched: Number of moves searched before deciding
        """

        # Moves searched counter
        moves_searched = 0

        # Get valid moves
        valid_moves = game.get_valid_moves()
        num_valid_moves = len(valid_moves)

        if num_valid_moves > 0:

            # Array of max score per next move
            max_scores = []

            # For each valid initial move
            for next_move in valid_moves:

                # Make initial move
                game_next = game.deepcopy()
                game_next.make_move(next_move)
                moves_searched += 1
                next_score = game_next.get_score()

                # Recursively search next moves
                if self._search_depth > 1:
                    agent = ExhaustiveSearchAgent(self._search_depth - 1)
                    next_next_move, next_moves_searched = agent.select_move(game_next)
                    moves_searched += next_moves_searched
                    if next_next_move is not None:
                        game_next.make_move(next_next_move)
                        moves_searched += 1
                        max_score = game_next.get_score()
                        max_scores.append(max_score)
                    else:
                        max_scores.append(next_score)
                else:
                    max_scores.append(next_score)

            # Select move with highest max score
            move = valid_moves[np.argmax(max_scores)]
            return move, moves_searched
        else:
            return None, 0
