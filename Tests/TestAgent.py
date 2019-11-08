"""
TestAgent.py
Test function for evaluating Square Stacker AI agents
"""

import numpy as np
import matplotlib.pyplot as plt
from Utilities.ProgressTracker import ProgressTracker
from SquareStackerGame import SquareStackerGame


def test_agent(agent, num_games=10000, num_bins=20):
    """
    Tests given Square Stacker agent by running games
    :param agent: Square Stacker AI agent
    :param num_games: Number of games to test
    :param num_bins: Number of histogram bins
    :return mean: Mean of scores
    :return std: Standard deviation of scores
    :return min_: Min score
    :return max_: Max score
    """

    # Play games and track scores
    progress = ProgressTracker(1.0)
    progress.start()
    scores = [0] * num_games

    print('Square Stacker Agent Test')
    print(f'Playing {num_games} games...\n')

    for i in range(num_games):

        # Play game until no valid moves exist
        game = SquareStackerGame()
        while True:

            # Generate valid moves
            valid_moves = game.get_valid_moves()
            num_valid_moves = len(valid_moves)

            if num_valid_moves > 0:
                # Make move according to agent
                move = agent.select_move(game)
                game.make_move(move)
            else:
                # Log score and exit game
                scores[i] = game.get_score()
                break

        # Update progress printer
        progress.update(float(i + 1) / num_games)

    print('\nComplete!\n')

    # Summary statistics
    mean = np.mean(scores)
    std = np.std(scores)
    min_ = np.min(scores)
    max_ = np.max(scores)
    print('Score Stats:')
    print(f'Mean: {mean:.2f}')
    print(f'Std: {std:.2f}')
    print(f'Min: {min_}')
    print(f'Max: {max_}')

    # Plot histogram of scores
    fig, axs = plt.subplots(1, 1)
    axs.hist(scores, bins=num_bins)
    axs.set_title('Random Agent Scores')
    axs.set_xlabel('Score')
    axs.set_ylabel('Frequency')
    plt.show()

    # Return summary stats
    return mean, std, min_, max_
