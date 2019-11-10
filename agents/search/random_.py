"""
random_.py
Class for Square Stacker Random search Agent

AI plays the game by the following process:
- For each move, play N games to completion with random moves
- Find the average end score for each move
- Make the move with the highest average score
- Repeat the process

Reference: https://ronzil.github.io/2048-AI/
"""

import numpy as np
from agents.search.agent import SearchAgent
from agents.random import RandomAgent


class RandomSearchAgent(SearchAgent):

    def __init__(self, games_per_move):
        """
        Constructs random search agent
        :param games_per_move: Games to play per possible move
        """
        SearchAgent.__init__(self)
        self._games_per_move = games_per_move
        self._random_agent = RandomAgent()

    def select_move(self, game):
        """
        Selects next move to make for given game
        :param game: Current game [SquareStackerGame]
        :return move: Move [k, i, j] or None if no moves exist
        :return moves_searched: Number of moves searched before deciding
        """

        # Moves searched counter
        moves_searched = 0

        # Get valid moves
        valid_moves = game.get_valid_moves()
        num_valid_moves = len(valid_moves)

        if num_valid_moves > 0:

            # Array of mean scores per next move
            mean_scores = []

            # For each valid initial move
            for next_move in valid_moves:

                # Make initial move
                game_next = game.deepcopy()
                game_next.make_move(next_move)
                moves_searched += 1

                # Play N games with random agent
                mean_score = 0.0
                for g in range(self._games_per_move):
                    game_test = game_next.deepcopy()
                    while True:
                        test_move = self._random_agent.select_move(game_test)
                        if test_move is not None:
                            game_test.make_move(test_move)
                            moves_searched += 1
                        else:
                            break
                    mean_score += game_test.get_score()
                mean_score /= self._games_per_move

                # Compute mean score
                mean_scores.append(mean_score)

            # Select move with highest mean score
            move = valid_moves[np.argmax(mean_scores)]
            return move, moves_searched
        else:
            return None, moves_searched
